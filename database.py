import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    event_type TEXT,
    event_time TEXT,
    metadata_json TEXT
)
""")
conn.commit()

def insert_event(event):
    cursor.execute("""
        INSERT INTO events (user_id, event_type, event_time, metadata_json)
        VALUES (?, ?, ?, ?)
    """, (
        event['user_id'],
        event['event_type'],
        event['timestamp'],
        json.dumps(event['metadata'])
    ))
    conn.commit()

def should_trigger_ml(user_id):
    window_end = datetime.utcnow()
    window_start = window_end - timedelta(minutes=5)
    cursor.execute("""
        SELECT COUNT(*) FROM events
        WHERE user_id = ?
        AND event_time BETWEEN ? AND ?
    """, (user_id, window_start.isoformat(), window_end.isoformat()))
    count = cursor.fetchone()[0]
    return count >= 10