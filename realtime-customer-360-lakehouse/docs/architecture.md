# Architecture

```mermaid
flowchart LR
  A[PostgreSQL CRM / APIs] --> B[Kafka CDC - planned]
  B --> C[Spark Streaming - planned]
  C --> D[Delta Bronze - planned]
  D --> E[Delta Silver / CDC MERGE - planned]
  E --> F[Customer 360 Gold - planned]
  F --> G[BI / Snowflake - planned]
```

**Local runnable slice:** JSONL events → validation/quarantine → ordered CDC merge → current customer view.

**CDC rules:** `UPSERT` or `DELETE`; later event timestamps win, event_id breaks ties; invalid IDs/emails quarantined. Deletes produce tombstones in current view. In production, ordering requires source LSN/sequence and partition-key guarantees, not timestamps alone.
