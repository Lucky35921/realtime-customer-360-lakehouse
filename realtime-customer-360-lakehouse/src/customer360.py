"""Minimal, runnable Customer 360 CDC prototype (Python standard library)."""
import argparse
import json
from pathlib import Path


def validate(event):
    if not event.get("event_id") or not event.get("customer_id") or not event.get("event_time"):
        return "missing event_id, customer_id or event_time"
    if event.get("op") not in {"UPSERT", "DELETE"}:
        return "unsupported operation"
    if event["op"] == "UPSERT" and "@" not in str(event.get("email", "")):
        return "invalid email"
    return None


def build_view(events):
    state, quarantine, seen = {}, [], set()
    for event in events:
        error = validate(event)
        if error:
            quarantine.append({"reason": error, "event": event})
            continue
        if event["event_id"] in seen:
            continue
        seen.add(event["event_id"])
        cid = event["customer_id"]
        prior = state.get(cid)
        if prior is None or (event["event_time"], event["event_id"]) > (prior["event_time"], prior["event_id"]):
            state[cid] = event
    customers = [dict(customer_id=cid, name=e.get("name"), email=e.get("email"), city=e.get("city"), updated_at=e["event_time"])
                 for cid, e in sorted(state.items()) if e["op"] != "DELETE"]
    return customers, quarantine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output")
    args = parser.parse_args()
    events = [json.loads(line) for line in Path(args.input).read_text().splitlines() if line.strip()]
    customers, quarantine = build_view(events)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "customer_360.json").write_text(json.dumps(customers, indent=2) + "\n")
    (out / "quarantine.json").write_text(json.dumps(quarantine, indent=2) + "\n")
    print(f"Customer 360 rows: {len(customers)}; quarantined: {len(quarantine)}")

if __name__ == "__main__":
    main()
