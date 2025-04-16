from confluent_kafka import Producer
import json
import random
from datetime import datetime, timedelta
import time

p = Producer({'bootstrap.servers': 'localhost:9092'})

user_ids = ['user_1', 'user_2']
event_types = ['click', 'view', 'purchase']
now = datetime.utcnow()

def generate_event():
    event = {
        "user_id": random.choice(user_ids),
        "event_type": random.choice(event_types),
        "timestamp": (now - timedelta(minutes=random.randint(0, 4), seconds=random.randint(0, 59))).isoformat(),
        "metadata": {
            "browser": random.choice(["Chrome", "Firefox", "Safari"]),
            "location": random.choice(["US", "CA", "EU"])
        }
    }
    return json.dumps(event)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered message to {msg.topic()} [{msg.partition()}]")

for _ in range(15):
    event_data = generate_event()
    p.produce('user_events', event_data.encode('utf-8'), callback=delivery_report)
    p.poll(0)
    time.sleep(0.2)

p.flush()