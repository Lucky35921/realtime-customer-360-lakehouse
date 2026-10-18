import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fraud_stream import analyze

class TestFraud(unittest.TestCase):
    def test_high_value_and_dedup(self):
        event = {"transaction_id":"1","account_id":"A","amount":6000,"event_time":"2026-01-01T00:00:00Z"}
        alerts, quarantine = analyze([event, event])
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["reasons"], ["HIGH_VALUE"])
        self.assertFalse(quarantine)

if __name__ == "__main__": unittest.main()
