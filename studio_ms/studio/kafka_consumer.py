import json
import os

import django

from kafka import KafkaConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studio.settings")
django.setup()

from app.listeners import order_created
from app.models import KafkaError


consumer = KafkaConsumer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))


def kafka_python_consumer():
    consumer.subscribe([os.getenv("MQ_ORDER_CREATED")])
    for msg in consumer:
        # print(
        #     "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
        #         msg.topic, msg.partition, msg.offset, msg.key, msg.value,
        #         msg.timestamp)
        # )

        value = msg.value

        try:
            order_created(json.loads(value.decode()))
        except Exception as e:
            print(e)

            KafkaError.objects.create(
                # key=msg.key(),
                key="order_created",
                value=value.decode(),
                error=e,
            )


kafka_python_consumer()
