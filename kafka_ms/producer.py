import os
from kafka import KafkaProducer

msg = ("kafka" * 20).encode()[:100]
size = 10
producer = KafkaProducer(bootstrap_servers=os.getenv("BOOTSTRAP_SERVERS"))


def kafka_python_producer_sync(producer, size):
    for _ in range(size):
        future = producer.send('order_created', msg)
        result = future.get(timeout=60)
    producer.flush()


kafka_python_producer_sync(producer, size)

