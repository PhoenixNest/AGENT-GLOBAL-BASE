---
title: 'Data Pipeline Ownership: Kafka → Data Lake → BI'
owner: 'Dr. Priya Mehta, CIO'
created: '2026-04-12'
status: 'Draft'
stage: '4'
audit-condition: 'C4'
tags: ['data-pipeline', 'kafka', 'data-lake', 'bi', 'ownership', 'analytics']
---

# Data Pipeline Ownership: Kafka → Data Lake → BI

> **CIO Audit Finding C4:** _"Kafka → Data Lake → BI segment has no identified owner."_
>
> This document assigns ownership, defines the pipeline architecture, and establishes the delivery timeline across development stages.

---

## Executive Summary

Per CIO audit finding C4, the **Kafka → Data Lake → BI data pipeline segment had no identified owner**. This is a critical gap: without clear ownership, the pipeline risks becoming an unmanaged dependency that blocks analytics, compliance reporting, and live ops decision-making.

This document resolves C4 by:

1. **Assigning named owners** for each pipeline segment
2. **Defining the technical architecture** for data flow from PlayFab events to BI dashboards
3. **Establishing governance** for data quality, access control, and COPPA compliance
4. **Mapping deliverables** to pipeline stages 3 through 8

---

## 1. Pipeline Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE: PlayFab → BI Dashboards                     │
│                                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐ │
│  │  PlayFab    │────▶│   Kafka     │────▶│  Data Lake  │────▶│     BI      │ │
│  │  Events     │     │  (Stream)   │     │  (Storage)  │     │ Dashboards  │ │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘ │
│        │                   │                   │                   │          │
│   Segment 0            Segment 1           Segment 2           Segment 3      │
│   (Source)          (Ingestion)          (Storage)          (Analytics)       │
│                                                                              │
│   Owner:              Owner:              Owner:              Owner:          │
│   PlayFab             Aisha Bello         David Okafor        Yuki Tanaka     │
│   (Platform)         Backend Engineer    Live Ops Engineer   Data Analyst     │
│                                                                              │
│   ──────────────────── Segment 0 + 1 ────────────────────                    │
│   PlayFab Events → Kafka: Real-time event ingestion                          │
│                                                                              │
│   ──────────────────── Segment 2 ────────────────────                        │
│   Kafka → Data Lake: Stream-to-batch materialization                        │
│                                                                              │
│   ──────────────────── Segment 3 ────────────────────                        │
│   Data Lake → BI: Query and dashboard layer                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Segment Ownership Assignment

### Segment 0: PlayFab Event Sources (Platform-Native)

| Attribute          | Detail                                                                              |
| ------------------ | ----------------------------------------------------------------------------------- |
| **Description**    | PlayFab platform emits events (player actions, economy transactions, custom events) |
| **Owner**          | PlayFab (managed service) — no internal ownership required                          |
| **Integration**    | PlayFab Event Hub / Event Grid integration to Kafka                                 |
| **Configuration**  | Event routing configured by Live Ops (David Okafor)                                 |
| **Events Catalog** | Maintained by Data Analyst (Yuki Tanaka)                                            |

### Segment 1: PlayFab Events → Kafka

| Attribute            | Detail                                                                                  |
| -------------------- | --------------------------------------------------------------------------------------- |
| **Description**      | Real-time ingestion of PlayFab events into Kafka cluster                                |
| **Owner**            | **Aisha Bello, Backend Engineer**                                                       |
| **Technology**       | Kafka cluster (self-hosted or managed: Confluent Cloud / MSK)                           |
| **Integration**      | PlayFab Webhook → API Gateway → Kafka Producer **OR** PlayFab Event Hub → Kafka Connect |
| **Responsibilities** | Kafka cluster provisioning, topic management, consumer group management, monitoring     |
| **SLA**              | Event ingestion latency ≤ 5 seconds P99; 99.9% availability                             |

### Segment 2: Kafka → Data Lake (S3 / Azure Blob)

| Attribute            | Detail                                                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| **Description**      | Stream-to-batch materialization: Kafka topics → persistent object storage                       |
| **Owner**            | **David Okafor, Live Ops Engineer** (infrastructure); **Yuki Tanaka** (schema requirements)     |
| **Technology**       | Kafka Connect with S3 Sink Connector (AWS) **or** Azure Blob Sink Connector (Azure)             |
| **Schema**           | Parquet format, partitioned by `date/event_type/tenant_id`                                      |
| **Retention**        | 90 days hot storage (frequent query), 1 year cold storage (Glacier / Azure Archive)             |
| **Responsibilities** | Connector configuration, schema evolution, storage cost optimization, data lifecycle management |

### Segment 3: Data Lake → BI Dashboards

| Attribute            | Detail                                                                                               |
| -------------------- | ---------------------------------------------------------------------------------------------------- |
| **Description**      | Query layer and dashboarding over data lake contents                                                 |
| **Owner**            | **Yuki Tanaka, Data Analyst** (dashboard design, data catalog); **David Okafor** (query performance) |
| **Technology**       | Athena (S3) or Synapse (Azure Blob) for SQL querying; Metabase or Redash for dashboards              |
| **Responsibilities** | Dashboard design, data catalog maintenance, data quality checks, stakeholder reporting               |

---

## 3. Segment 2 Detail: Kafka → Data Lake

### 3.1 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Kafka Connect: Kafka → Data Lake (Segment 2)                    │
│                                                                  │
│  ┌───────────┐     ┌──────────────┐     ┌────────────────────┐  │
│  │  Kafka    │────▶│  Kafka       │────▶│  S3 / Azure Blob   │  │
│  │  Topics   │     │  Connect     │     │  (Data Lake)       │  │
│  │           │     │  Workers     │     │                    │  │
│  └───────────┘     └──────────────┘     └────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│                    ┌────────────────────┐                        │
│                    │  Schema Registry   │                        │
│                    │  (Avro/Protobuf)   │                        │
│                    └────────────────────┘                        │
│                                                                  │
│  Output Format: Parquet                                          │
│  Partitioning: s3://bucket/events/date=YYYY-MM-DD/type=EVENT/    │
│  Batch Size: 10,000 records or 10 minutes (whichever first)     │
│  Compression: Snappy                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Schema Definition

| Field             | Type      | Description                            | Source             |
| ----------------- | --------- | -------------------------------------- | ------------------ |
| `event_id`        | UUID      | Unique event identifier                | PlayFab / Producer |
| `tenant_id`       | String    | PlayFab Title ID                       | PlayFab            |
| `event_type`      | String    | Event classification                   | PlayFab            |
| `event_timestamp` | Timestamp | UTC timestamp of event occurrence      | PlayFab            |
| `player_id`       | String    | Anonymized player identifier           | PlayFab            |
| `event_data`      | JSON      | Event payload (type-specific schema)   | PlayFab            |
| `ingestion_ts`    | Timestamp | Timestamp of Kafka ingestion           | Kafka Connect      |
| `lake_ts`         | Timestamp | Timestamp of Data Lake materialization | Kafka Connect      |

### 3.3 Storage Lifecycle

| Tier     | Storage Class              | Retention       | Access Pattern     | Cost Tier |
| -------- | -------------------------- | --------------- | ------------------ | --------- |
| **Hot**  | S3 Standard / Azure Hot    | 90 days         | Frequent queries   | High      |
| **Warm** | S3 IA / Azure Cool         | 90–180 days     | Infrequent queries | Medium    |
| **Cold** | S3 Glacier / Azure Archive | 180 days–1 year | Compliance, audit  | Low       |

---

## 4. Segment 3 Detail: Data Lake → BI

### 4.1 Query Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  BI Query Layer (Segment 3)                                      │
│                                                                  │
│  ┌──────────────────┐     ┌──────────────┐     ┌──────────────┐ │
│  │  Data Lake       │────▶│  Athena /    │────▶│  Metabase /  │ │
│  │  (Parquet/S3)    │     │  Synapse     │     │  Redash      │ │
│  │                  │     │  (Query)     │     │  (Dashboard) │ │
│  └──────────────────┘     └──────────────┘     └──────────────┘ │
│         │                       │                      │         │
│         ▼                       ▼                      ▼         │
│   ┌──────────┐          ┌──────────┐          ┌──────────┐      │
│   │ Schema   │          │ Query    │          │ Dashboard│      │
│   │ Catalog  │          │ Cache    │          │ Library  │      │
│   │ (Yuki)   │          │ (David)  │          │ (Yuki)   │      │
│   └──────────┘          └──────────┘          └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Dashboard Portfolio (Owned by Yuki Tanaka)

| Dashboard             | Audience           | Refresh Rate | Data Source             |
| --------------------- | ------------------ | ------------ | ----------------------- |
| Daily Active Users    | Product / Live Ops | 1 hour       | Player events           |
| Revenue & IAP Metrics | Product / Finance  | 4 hours      | Economy transactions    |
| Retention Cohorts     | Product            | Daily        | Login/session events    |
| Technical Performance | Engineering        | 1 hour       | Error/crash events      |
| COPPA Compliance      | Legal / CSO        | Daily        | All events (audit)      |
| Pipeline Health       | Engineering        | 15 minutes   | Kafka/Data Lake metrics |

---

## 5. Data Governance

### 5.1 Roles and Responsibilities

| Responsibility          | Owner        | Backup                | Description                                               |
| ----------------------- | ------------ | --------------------- | --------------------------------------------------------- |
| **Data Catalog**        | Yuki Tanaka  | Aisha Bello           | Maintain event dictionary, schema registry, field lineage |
| **Access Control**      | David Okafor | Dr. Sarah Chen (CSO)  | IAM policies for Data Lake, BI tool, Kafka topics         |
| **Data Quality Checks** | Yuki Tanaka  | Priscilla Oduya       | Automated validation: completeness, freshness, accuracy   |
| **COPPA Compliance**    | CSO Office   | David Okafor          | Data retention enforcement, PII masking, audit trails     |
| **Pipeline Monitoring** | Aisha Bello  | David Okafor          | Kafka lag, connector health, storage utilization          |
| **Cost Optimization**   | David Okafor | Dr. Priya Mehta (CIO) | Storage tiering, query cost, Kafka cluster sizing         |

### 5.2 COPPA Compliance Enforcement

Per `security.md`, the CSO Office retains ownership of COPPA compliance enforcement. The data pipeline must support:

- **PII Masking:** Player identifiers anonymized at ingestion (Segment 1); no raw PII stored in Data Lake
- **Data Retention:** Automatic deletion of under-13 player data per retention policy; enforced at storage tier (Segment 2)
- **Audit Trail:** All data access logged; CSO Office can audit any query or dashboard access
- **Consent Tracking:** Player consent status stored alongside events; consent withdrawal triggers data deletion cascade

### 5.3 Access Control Matrix

| Role         | Kafka (Read) | Kafka (Write) | Data Lake (Read) | Data Lake (Write) | BI (Read) | BI (Admin) |
| ------------ | :----------: | :-----------: | :--------------: | :---------------: | :-------: | :--------: |
| Aisha Bello  |      ✅      |      ✅       |        ❌        |        ❌         |    ❌     |     ❌     |
| David Okafor |      ✅      |      ❌       |        ✅        |        ✅         |    ❌     |     ❌     |
| Yuki Tanaka  |      ❌      |      ❌       |        ✅        |        ❌         |    ✅     |     ✅     |
| CSO Office   |      ❌      |      ❌       | ✅ (audit only)  |        ❌         |    ❌     |     ❌     |
| CIO          |      ✅      |      ❌       |        ✅        |        ❌         |    ✅     |     ❌     |

---

## 6. Timeline and Stage Mapping

| Stage  | Deliverable                                                    | Owner(s)                                          | Gate Criteria                                      |
| ------ | -------------------------------------------------------------- | ------------------------------------------------- | -------------------------------------------------- |
| **3**  | Kafka → Data Lake connector design documented                  | Aisha Bello, David Okafor                         | Architecture review; ADR completed                 |
| **4**  | Data Lake schema defined; BI dashboard requirements documented | David Okafor, Yuki Tanaka                         | Implementation Plan includes pipeline              |
| **5**  | Pipeline operational for internal testing data                 | Aisha Bello (Segment 1), David Okafor (Segment 2) | End-to-end event flow verified                     |
| **7**  | Pipeline operational for soft launch data                      | All owners                                        | Test Results Report includes pipeline metrics      |
| **8**  | Pipeline operational for production data                       | All owners                                        | Integrity Verification confirms pipeline integrity |
| **10** | Pipeline included in Release Readiness checklist               | Yuki Tanaka (dashboard sign-off)                  | Release Checklist item: Analytics operational      |

---

## 7. Cost Estimate

| Component                   | Monthly Cost (Est.) | Notes                                      |
| --------------------------- | ------------------- | ------------------------------------------ |
| Kafka cluster (3 brokers)   | $150–300            | Self-hosted on existing compute or managed |
| Kafka Connect workers       | $50–100             | Can share broker compute at small scale    |
| Data Lake storage (90d hot) | $20–50              | ~50GB/month for 3 games at casual scale    |
| Athena / Synapse queries    | $10–30              | Cost scales with query volume              |
| BI tool (Metabase OSS)      | $0 (self-hosted)    | Metabase Cloud: $85/month (optional)       |
| **Total**                   | **$230–480/month**  | Scales with player count and event volume  |

---

## 8. Review and Escalation

| Item                 | Detail                                           |
| -------------------- | ------------------------------------------------ |
| **Document Owner**   | Dr. Priya Mehta, CIO                             |
| **Segment 1 Owner**  | Aisha Bello, Backend Engineer                    |
| **Segment 2 Owner**  | David Okafor, Live Ops Engineer                  |
| **Segment 3 Owner**  | Yuki Tanaka, Data Analyst                        |
| **CSO Consultation** | Dr. Sarah Chen (COPPA compliance)                |
| **Status**           | Draft — pending Stage 4 gate review              |
| **Re-assessment**    | Quarterly, or when player count exceeds 100K MAU |

### Escalation Path

| Issue                              | Escalate To          | Timeline  |
| ---------------------------------- | -------------------- | --------- |
| Pipeline lag > 60 seconds          | Aisha Bello → CTO    | Immediate |
| Data quality check failure         | Yuki Tanaka → CIO    | 4 hours   |
| Storage cost exceeds budget by 20% | David Okafor → CIO   | 24 hours  |
| COPPA compliance violation         | CSO Office → C-Suite | Immediate |

---

_This document satisfies CIO Audit Condition C4. Ownership is assigned, architecture is defined, and delivery is mapped to pipeline stages 3 through 8._
