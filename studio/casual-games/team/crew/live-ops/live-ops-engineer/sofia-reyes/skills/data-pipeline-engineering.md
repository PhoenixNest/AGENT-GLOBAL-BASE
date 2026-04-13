---
name: data-pipeline-engineering
description: Real-time and batch data pipeline architecture for game analytics, using Kafka, Flink, ClickHouse, and cloud storage.
---

# Data Pipeline Engineering

## Overview

This skill covers the design, implementation, and maintenance of data pipelines for live game analytics, supporting real-time experiment monitoring, player behavior analysis, and LTV forecasting.

## Pipeline Architecture

### Streaming Pipeline (Real-Time)

| Component  | Technology | Purpose                        | SLA                 |
| ---------- | ---------- | ------------------------------ | ------------------- |
| Ingestion  | Kafka      | Event buffering, ordering      | < 100ms latency     |
| Processing | Flink      | Stream processing, aggregation | Exactly-once        |
| Serving    | ClickHouse | Real-time queries, dashboards  | < 1s query time     |
| Monitoring | Prometheus | Pipeline health, lag tracking  | 15s scrape interval |

### Batch Pipeline (Analytical)

| Component | Technology   | Purpose                            | Frequency        |
| --------- | ------------ | ---------------------------------- | ---------------- |
| Storage   | S3 (Parquet) | Raw event data, compressed         | Daily partitions |
| Transform | dbt / Spark  | Data cleaning, feature engineering | Daily            |
| Serving   | BigQuery     | Ad-hoc analysis, ML features       | On-demand        |

### Data Quality Checks

| Check Type        | Method                      | Alert Threshold   |
| ----------------- | --------------------------- | ----------------- |
| Completeness      | Row count vs. expected      | < 95% of expected |
| Freshness         | Last event timestamp        | > 5 minutes lag   |
| Schema validation | Column types, null checks   | Any schema drift  |
| Anomaly detection | Statistical process control | > 3σ deviation    |
