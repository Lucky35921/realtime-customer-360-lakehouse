# Real-Time Customer 360 Lakehouse

## Target Architecture

![Real-Time Customer 360 Architecture](docs/architecture.png)

## Project Overview

A real-time data engineering lakehouse designed using
Apache Kafka, PySpark, Delta Lake, and Databricks.


**Status: Working local CDC prototype; Kafka, Spark, Delta Lake, Databricks and Airflow integrations are planned.**

An independent Customer 360 project using **synthetic CRM customer events** (not NYC Taxi data). Demonstrates change-data-capture upserts, deduplication, late-event protection, data-quality quarantine, and a customer 360 current-state table.

## Target architecture
PostgreSQL / APIs → Kafka → Spark Structured Streaming → Delta Lake Bronze/Silver/Gold → Databricks → Snowflake / Power BI

## Implemented locally
- Read JSONL customer CDC events; preserve append-only bronze events.
- Validate customer ID, email, and operation; quarantine invalid events.
- Apply last-write-wins CDC merge using event timestamps and event IDs.
- Materialize `customer_360.json` and `quarantine.json`.
- Standard-library unit tests.

## Run
```bash
python3 src/customer360.py --input sample_data/customer_events.jsonl --output output
python3 -m unittest discover -s tests -v
```

## Planned milestones
1. Add PostgreSQL Debezium CDC and Kafka topics.
2. Implement Spark Structured Streaming with Delta MERGE and checkpointing.
3. Add SCD Type 2 history, schema evolution and backfills.
4. Orchestrate with Airflow; add observability and CI/CD.

See `docs/architecture.md`. Synthetic sample data only. No production throughput or cloud deployment claims.
