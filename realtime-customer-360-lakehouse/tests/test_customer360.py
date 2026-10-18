import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from customer360 import build_view

class TestCustomer360(unittest.TestCase):
    def test_upsert_delete_and_invalid(self):
        events = [
            {"event_id":"1","customer_id":"A","op":"UPSERT","event_time":"2026-01-01","email":"a@b.com","name":"A"},
            {"event_id":"2","customer_id":"A","op":"DELETE","event_time":"2026-01-02"},
            {"event_id":"3","customer_id":"B","op":"UPSERT","event_time":"2026-01-03","email":"bad"},
        ]
        current, quarantine = build_view(events)
        self.assertEqual(current, [])
        self.assertEqual(len(quarantine), 1)

if __name__ == "__main__": unittest.main()
