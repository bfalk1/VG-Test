import json
from database import insert_event, should_trigger_ml

def validate_event(event):
    required_keys = {'user_id', 'event_type', 'timestamp', 'metadata'}
    return required_keys.issubset(event.keys())

def process_event(event_str):
    try:
        event = json.loads(event_str)
    except json.JSONDecodeError:
        print("Invalid JSON")
        return

    if not validate_event(event):
        print("Invalid event schema")
        return

    insert_event(event)
    if should_trigger_ml(event['user_id']):
        print(f"Triggering ML model for user_id: {event['user_id']}")