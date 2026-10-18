"""Local, ordered-event simulation of streaming fraud rules."""
import argparse
import json
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from pathlib import Path


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def analyze(events, high_value=5000.0, velocity_count=3, window_minutes=5):
    seen, history, alerts, quarantine = set(), defaultdict(deque), [], []
    for e in events:
        try:
            tid, account = e["transaction_id"], e["account_id"]
            amount, when = float(e["amount"]), timestamp(e["event_time"])
            if not tid or not account or amount <= 0 or when.tzinfo is None:
                raise ValueError("invalid transaction fields")
        except (KeyError, TypeError, ValueError) as exc:
            quarantine.append({"event": e, "reason": str(exc)})
            continue
        if tid in seen:
            continue
        seen.add(tid)
        h = history[account]
        while h and when - h[0] > timedelta(minutes=window_minutes):
            h.popleft()
        h.append(when)
        reasons = []
        if amount >= high_value:
            reasons.append("HIGH_VALUE")
        if len(h) >= velocity_count:
            reasons.append("HIGH_VELOCITY")
        if reasons:
            alerts.append({"transaction_id": tid, "account_id": account, "reasons": reasons, "amount": amount})
    return alerts, quarantine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output")
    args = parser.parse_args()
    events = [json.loads(line) for line in Path(args.input).read_text().splitlines() if line.strip()]
    # This prototype assumes events arrive in nondecreasing event_time order.
    alerts, quarantine = analyze(events)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "alerts.json").write_text(json.dumps(alerts, indent=2) + "\n")
    (out / "quarantine.json").write_text(json.dumps(quarantine, indent=2) + "\n")
    print(f"Alerts: {len(alerts)}; quarantined: {len(quarantine)}")

if __name__ == "__main__":
    main()
