from confluent_kafka import Consumer, KafkaException
from event_processor import process_event

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'event_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['user_events'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            process_event(msg.value().decode('utf-8'))
except KeyboardInterrupt:
    pass
finally:
    consumer.close()