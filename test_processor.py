import unittest
from event_processor import validate_event
from database import insert_event, should_trigger_ml

valid_event = {
    "user_id": "abc123",
    "event_type": "click",
    "timestamp": "2025-04-16T12:00:00",
    "metadata": {"browser": "Chrome"}
}

class TestEventProcessing(unittest.TestCase):
    def test_validation(self):
        self.assertTrue(validate_event(valid_event))
        self.assertFalse(validate_event({}))

    def test_trigger_logic(self):
        for _ in range(10):
            insert_event(valid_event)
        self.assertTrue(should_trigger_ml("abc123"))

if __name__ == '__main__':
    unittest.main()