from kafka import KafkaProducer

from app.config import settings


def send_sync(message: str):
    producer = KafkaProducer(bootstrap_servers=settings.BOOTSTRAP_SERVERS)
    future = producer.send(settings.MQ_ORDER_CREATED, message.encode())
    result = future.get(timeout=60)
    producer.flush()
