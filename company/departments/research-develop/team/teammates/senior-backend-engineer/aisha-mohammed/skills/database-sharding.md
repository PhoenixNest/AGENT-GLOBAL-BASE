---
version: "1.0.0"
---

| Competency                  | Description                                                             | Quality Criteria                                                                                                                                   |
| --------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Horizontal Partitioning     | Sharding vs partitioning distinction, shard topology, data distribution | Designs shard architecture that scales linearly; can explain why sharding is a last resort after vertical scaling, read replicas, and partitioning |
| Sharding Strategies         | Hash-based, range-based, directory-based, geo-based                     | Selects strategy based on access patterns; implements consistent hashing for hash-based sharding to minimize rebalancing impact                    |
| Distributed Query Execution | Cross-shard queries, scatter-gather, query routing, aggregation         | Designs queries that minimize cross-shard operations; implements efficient scatter-gather with partial result merging                              |
| Eventual Consistency        | Consistency models, conflict resolution, read-your-writes guarantee     | Implements application-level consistency guarantees; handles replica lag across shards; designs conflict resolution for concurrent writes          |
| Failover Handling           | Shard-level failover, automatic promotion, split-brain prevention       | Designs failover runbooks per shard; implements automated failover with health checks; prevents split-brain with quorum-based decisions            |
| Rebalancing                 | Live data migration, hash ring adjustment, zero-downtime rebalancing    | Implements live rebalancing with dual-write during migration; monitors rebalancing progress with rollback capability                               |

## Execution Guidance

### Sharding vs Other Scaling Strategies

**Decision tree for scaling PostgreSQL:**

```
Query performance issues?
├── Read-heavy? → Read replicas (scales reads up to ~10x)
├── Write-heavy single table? → Table partitioning (scales within single instance)
├── Data size exceeds single instance? →
│   ├── < 5TB? → Vertical scaling (larger instance)
│   └── > 5TB? → Sharding (last resort)
└── Connection limit reached? → Connection pooling (PgBouncer)
```

**Sharding adds operational complexity. Only shard when:**

- Single instance cannot handle write throughput (> 10K writes/sec)
- Data size exceeds practical single-instance limits (> 5-10TB with indexes)
- Multi-region latency requirements demand data locality
- Compliance requires data isolation per tenant/region

### Sharding Key Selection

**Critical decision — cannot be changed without full data migration:**

| Sharding Key          | Pros                                                     | Cons                                         | Best For                          |
| --------------------- | -------------------------------------------------------- | -------------------------------------------- | --------------------------------- |
| User ID               | All user data co-located; efficient user-centric queries | Hot shards for power users                   | User-facing apps, social networks |
| Tenant ID             | Complete tenant isolation; easy compliance               | Uneven distribution (large vs small tenants) | Multi-tenant SaaS                 |
| Geographic region     | Data locality; compliance                                | Cross-region queries expensive               | Global apps, GDPR compliance      |
| Time-based (date)     | Natural data lifecycle; easy archival                    | Hot shard for current period                 | Time-series, logging, IoT         |
| Hash of composite key | Even distribution                                        | Related data may be scattered                | High-throughput, uniform access   |

### Hash-Based Sharding with Consistent Hashing

```go
type ConsistentHashRing struct {
    ring       *hashring.Map
    shards     map[string]*Shard
    replicas   int  // Virtual nodes per physical shard
}

type Shard struct {
    ID       string
    Host     string
    Port     int
    DBName   string
    Status   ShardStatus
    Weight   int  // For weighted distribution
}

func NewConsistentHashRing(shards []*Shard, replicas int) *ConsistentHashRing {
    chr := &ConsistentHashRing{
        ring:     hashring.New(nil),
        shards:   make(map[string]*Shard),
        replicas: replicas,
    }
    for _, shard := range shards {
        chr.AddShard(shard)
    }
    return chr
}

func (chr *ConsistentHashRing) AddShard(shard *Shard) {
    chr.shards[shard.ID] = shard
    // Add virtual nodes for distribution
    for i := 0; i < chr.replicas; i++ {
        vnode := fmt.Sprintf("%s#%d", shard.ID, i)
        chr.ring = chr.ring.Add(vnode)
    }
}

func (chr *ConsistentHashRing) GetShard(key string) *Shard {
    vnode, ok := chr.ring.GetNode(key)
    if !ok {
        return nil
    }
    shardID := strings.Split(vnode, "#")[0]
    return chr.shards[shardID]
}

func (chr *ConsistentHashRing) RemoveShard(shardID string) {
    for i := 0; i < chr.replicas; i++ {
        vnode := fmt.Sprintf("%s#%d", shardID, i)
        chr.ring = chr.ring.Remove(vnode)
    }
    delete(chr.shards, shardID)
}
```

**Why consistent hashing?** When adding/removing shards, only `1/N` of keys need to move (vs hash-based where `~50%` move). This is critical for live rebalancing.

### Range-Based Sharding

```sql
-- Shard routing table (stored in config database)
CREATE TABLE shard_routing (
    shard_id VARCHAR(36) PRIMARY KEY,
    range_start VARCHAR(255) NOT NULL,
    range_end VARCHAR(255) NOT NULL,
    host VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    dbname VARCHAR(64) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Example routing for tenant_id ranges
INSERT INTO shard_routing (shard_id, range_start, range_end, host, port, dbname) VALUES
    ('shard-01', '00000000', '3fffffff', 'db-shard-01.internal', 5432, 'app_shard_01'),
    ('shard-02', '40000000', '7fffffff', 'db-shard-02.internal', 5432, 'app_shard_02'),
    ('shard-03', '80000000', 'bfffffff', 'db-shard-03.internal', 5432, 'app_shard_03'),
    ('shard-04', 'c0000000', 'ffffffff', 'db-shard-04.internal', 5432, 'app_shard_04');
```

**Range-based shard router:**

```go
func (r *RangeRouter) RouteQuery(ctx context.Context, tenantID string, query string, args ...interface{}) (*sql.Rows, error) {
    shard := r.findShardForTenant(tenantID)
    if shard == nil {
        return nil, ErrNoShardForTenant
    }

    db, err := r.getConnection(shard)
    if err != nil {
        return nil, err
    }

    return db.QueryContext(ctx, query, args...)
}

func (r *RangeRouter) findShardForTenant(tenantID string) *ShardRouting {
    // Binary search on sorted range boundaries
    idx := sort.Search(len(r.ranges), func(i int) bool {
        return r.ranges[i].RangeStart > tenantID
    })
    if idx > 0 {
        candidate := r.ranges[idx-1]
        if tenantID >= candidate.RangeStart && tenantID <= candidate.RangeEnd {
            return candidate
        }
    }
    return nil
}
```

### Distributed Query Execution

**Single-shard query (optimal):**

```go
// If sharding key is known, route directly to single shard
func (e *QueryEngine) QueryByShardKey(ctx context.Context, shardKey string, query string) (*sql.Rows, error) {
    shard := e.hashRing.GetShard(shardKey)
    db := e.getConnection(shard)
    return db.QueryContext(ctx, query)
}
```

**Cross-shard query (scatter-gather):**

```go
type CrossShardResult struct {
    Rows    [][]map[string]interface{}
    Errors  []error
}

func (e *QueryEngine) ScatterGather(ctx context.Context, query string, args ...interface{}) (*CrossShardResult, error) {
    var wg sync.WaitGroup
    result := &CrossShardResult{
        Rows:   make([][]map[string]interface{}, len(e.shards)),
        Errors: make([]error, len(e.shards)),
    }

    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()

    for i, shard := range e.shards {
        wg.Add(1)
        go func(idx int, s *Shard) {
            defer wg.Done()

            db, err := e.getConnection(s)
            if err != nil {
                result.Errors[idx] = err
                return
            }

            rows, err := db.QueryContext(ctx, query, args...)
            if err != nil {
                result.Errors[idx] = err
                return
            }
            defer rows.Close()

            result.Rows[idx], _ = scanRows(rows)
        }(i, shard)
    }

    wg.Wait()
    return result, nil
}

// Merge results from all shards (example: UNION ALL)
func MergeResults(results *CrossShardResult) ([]map[string]interface{}, error) {
    var merged []map[string]interface{}
    for _, shardRows := range results.Rows {
        merged = append(merged, shardRows...)
    }

    // Check for partial failures
    var failedShards int
    for _, err := range results.Errors {
        if err != nil {
            failedShards++
        }
    }
    if failedShards > 0 {
        return merged, fmt.Errorf("partial failure: %d/%d shards failed", failedShards, len(results.Errors))
    }

    return merged, nil
}
```

**Cross-shard query performance optimization:**

| Strategy                | Description                                            | When to Use                            |
| ----------------------- | ------------------------------------------------------ | -------------------------------------- |
| Denormalized read model | Maintain separate read-optimized store (Elasticsearch) | Complex search/filtering across shards |
| Materialized view       | Pre-computed cross-shard aggregations                  | Reporting, analytics                   |
| Application-level join  | Fetch from multiple shards, join in app                | Small result sets, infrequent queries  |
| Avoid entirely          | Redesign to include sharding key in query              | Preferred approach                     |

### Failover Handling

**Shard-level failover with automatic promotion:**

```go
type ShardFailoverManager struct {
    shards       map[string]*Shard
    healthChecker *HealthChecker
    promoter     *Promoter
}

func (m *ShardFailoverManager) Monitor(ctx context.Context) {
    ticker := time.NewTicker(10 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            for _, shard := range m.shards {
                if shard.Status == StatusActive {
                    healthy, err := m.healthChecker.Check(ctx, shard)
                    if err != nil || !healthy {
                        m.handleFailover(ctx, shard)
                    }
                }
            }
        case <-ctx.Done():
            return
        }
    }
}

func (m *ShardFailoverManager) handleFailover(ctx context.Context, failedShard *Shard) {
    log.Warnf("Shard %s failed health check, initiating failover", failedShard.ID)

    // 1. Mark shard as degraded
    failedShard.Status = StatusDegraded
    m.updateHashRing()

    // 2. Promote replica (if exists)
    replica, err := m.promoter.PromoteReplica(ctx, failedShard)
    if err != nil {
        log.Errorf("Failed to promote replica for shard %s: %v", failedShard.ID, err)
        // 3. If no replica, redistribute keys to remaining shards
        m.redistributeKeys(ctx, failedShard)
        return
    }

    // 4. Update routing to point to promoted replica
    m.updateShardRouting(failedShard.ID, replica)
    failedShard.Status = StatusFailed
    log.Infof("Shard %s failover complete, promoted %s", failedShard.ID, replica.ID)
}
```

**Split-brain prevention:**

```
Quorum-based decision:
  Total nodes: 3 (1 primary, 2 replicas)
  Quorum: 2 (majority)

  Decision to promote replica requires:
    - Primary confirmed unreachable (health check from ≥2 nodes)
    - Replica has replicated all WAL up to promotion point
    - ETCD/Consensus confirms no conflicting promotion in progress

  ETCD lease mechanism:
    - Primary holds lease with 15s TTL
    - Lease renewal every 5s
    - If lease expires, replicas can compete for promotion
    - Only one replica acquires promotion lock (ETCD transaction)
```

### Live Rebalancing

**Zero-downtime rebalancing with dual-write:**

```
Phase 1 — PREPARE: New shard provisioned, catch-up replication started
Phase 2 — DUAL-WRITE: Writes go to both source and target shard
Phase 3 — BACKFILL: Historical data copied from source to target
Phase 4 — VERIFY: Checksum comparison between source and target
Phase 5 — CUTOVER: Reads switch to new shard, dual-write stops
Phase 6 — CLEANUP: Old shard data archived, routing table updated
```

```go
type Rebalancer struct {
    sourceShard *Shard
    targetShard *Shard
    keyRange    KeyRange
}

func (r *Rebalancer) Execute(ctx context.Context) error {
    // Phase 1: Provision target
    if err := r.provisionTarget(ctx); err != nil {
        return fmt.Errorf("provision target: %w", err)
    }

    // Phase 2: Enable dual-write
    r.enableDualWrite(r.keyRange, r.targetShard)

    // Phase 3: Backfill historical data
    if err := r.backfill(ctx); err != nil {
        r.disableDualWrite(r.keyRange)
        return fmt.Errorf("backfill: %w", err)
    }

    // Phase 4: Verify data consistency
    if err := r.verifyConsistency(ctx); err != nil {
        r.disableDualWrite(r.keyRange)
        return fmt.Errorf("verify: %w", err)
    }

    // Phase 5: Cutover reads
    r.updateRoutingTable(r.keyRange, r.targetShard)
    r.disableDualWrite(r.keyRange)

    // Phase 6: Cleanup
    r.archiveSource(ctx)

    return nil
}
```

**Rebalancing monitoring:**

| Metric                       | Alert Threshold                  | Action                        |
| ---------------------------- | -------------------------------- | ----------------------------- |
| Rebalancing progress         | < 10% per hour (for 1TB dataset) | Investigate I/O bottleneck    |
| Dual-write latency increase  | > 50% baseline                   | Slow down backfill rate       |
| Source shard load            | > 80% CPU                        | Throttle backfill             |
| Target shard replication lag | > 30 seconds                     | Pause writes, catch up        |
| Data inconsistency           | > 0 rows mismatch                | Halt rebalancing, investigate |

## Pipeline Integration

**Stage 3 (Architecture):** Component diagrams must show shard topology, routing layer, and cross-shard query paths. ADR required for sharding key selection and sharding strategy (hash vs range vs directory).

**Stage 4 (Implementation Plan):** Shard provisioning is infrastructure dependency. Rebalancing implementation must be included as separate workstream. Failover runbooks must be authored before Stage 5.

**Stage 5 (Development):** Shard router implemented first. Application code updated to include sharding key in all queries. Cross-shard query minimization validated.

**Stage 6 (Code Review):** Review shard key inclusion in all queries. Validate routing logic correctness. Check dual-write implementation for rebalancing. Verify failover logic handles all edge cases.

**Stage 7 (Testing):** Load tests validate linear scaling with shard count. Failover tests validate automatic promotion. Rebalancing tests validate zero-downtime migration. Cross-shard query tests validate scatter-gather correctness.

**Stage 8 (Integrity Verification):** Panel verifies shard topology matches architecture, all queries include shard key (or use cross-shard path), failover runbooks tested, and rebalancing procedure validated.

## Quality Standards

| Metric                          | Target              | Measurement                 |
| ------------------------------- | ------------------- | --------------------------- |
| Shard distribution variance     | < 10% across shards | Shard size monitoring       |
| Single-shard query ratio        | > 90% of queries    | Query routing metrics       |
| Cross-shard query latency (p95) | < 2 seconds         | Distributed tracing         |
| Failover detection time         | < 15 seconds        | Health check monitoring     |
| Failover completion time        | < 60 seconds        | Failover runbook timing     |
| Rebalancing downtime            | 0 seconds           | Deployment metrics          |
| Data consistency post-rebalance | 100% match          | Checksum comparison         |
| Shard capacity headroom         | > 30% available     | Capacity planning dashboard |
