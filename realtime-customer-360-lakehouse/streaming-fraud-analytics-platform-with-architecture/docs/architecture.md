# Target architecture

```mermaid
flowchart LR
 A[Card transactions] --> B[Kafka / MSK - planned]
 B --> C[Spark Streaming - planned]
 C --> D[S3 Parquet - planned]
 D --> E[Glue Catalog - planned]
 E --> F[Redshift marts - planned]
 C --> G[Fraud alerts - planned]
```

**Local runnable slice:** JSONL event file → deduplication + rule engine → alert JSON / quarantine.

**Production considerations:** event-time windows and watermarks, state TTL, exactly-once sink semantics, replay safety, PII handling, rule calibration, and monitoring false positives.
