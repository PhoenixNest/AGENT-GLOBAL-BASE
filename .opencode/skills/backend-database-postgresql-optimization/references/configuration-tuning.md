# Configuration Tuning

## Configuration Tuning

### Memory Settings

```ini
# postgresql.conf — memory configuration

# shared_buffers: 25% of system RAM (up to 8GB, beyond that diminishing returns)
# 4GB RAM -> 1GB, 16GB RAM -> 4GB, 64GB RAM -> 8GB (cap at 8-12GB)
shared_buffers = 2GB

# effective_cache_size: estimate of OS disk cache available
# Set to 50-75% of total RAM
effective_cache_size = 12GB

# work_mem: per-operation memory for sorts, hashes, joins
# Total potential usage = work_mem * max_connections * operations
# Be conservative — this is PER operation, PER connection
work_mem = 64MB

# maintenance_work_mem: for VACUUM, CREATE INDEX, ALTER TABLE
# Can be large since few concurrent maintenance operations
maintenance_work_mem = 512MB

# huge_pages: try to reduce TLB pressure on large memory systems
huge_pages = try
```

### WAL and Durability

```ini
# Write-Ahead Log configuration

# wal_level: replica needed for streaming replication
wal_level = replica

# max_wal_senders: for replication and pg_basebackup
max_wal_senders = 5

# wal_buffers: auto-tuned from shared_buffers usually fine
# wal_buffers = -1  # default: auto-tune from shared_buffers (1/32, min 64kB)

# synchronous_commit: balance durability vs performance
# on = safe (default), off = ~1s data loss risk, 3x throughput gain
synchronous_commit = on

# checkpoint settings
checkpoint_completion_target = 0.9    -- spread checkpoint I/O over time
checkpoint_timeout = 15min            -- 5min default, increase for write-heavy
max_wal_size = 2GB                    -- 1GB default, increase for write-heavy
min_wal_size = 512MB                  -- 80MB default
```

### Query Planner Hints

```ini
# Enable/disable plan types (use as temporary diagnostics, not permanent fixes)
enable_seqscan = on          -- keep on; disabling seqscan rarely helps
enable_hashjoin = on
enable_nestloop = on
enable_bitmapscan = on

# Random page cost — lower for SSDs
random_page_cost = 1.1       -- 4.0 default (HDD), 1.1 for SSD/cloud

# Effective I/O concurrency — lower for cloud storage
effective_io_concurrency = 200  -- 1 default (HDD), 200 for SSD
```

---
