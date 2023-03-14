import os

from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(bootstrap_servers=os.getenv("BOOTSTRAP_SERVERS"))


def kafka_python_consumer():
    consumer.subscribe(['order_created'])
    for msg in consumer:
        print(msg)


kafka_python_consumer()


def kafka_python_consumer2():
    consumer2 = KafkaConsumer(bootstrap_servers=os.getenv("BOOTSTRAP_SERVERS"))
    consumer2.assign([TopicPartition('topic1', 1), TopicPartition('topic2', 1)])
    for msg in consumer2:
        print(msg)


def kafka_python_consumer3():
    consumer3 = KafkaConsumer(bootstrap_servers=os.getenv("BOOTSTRAP_SERVERS"))
    partition = TopicPartition('topic3', 0)
    consumer3.assign([partition])
    last_offset = consumer3.end_offsets([partition])[partition]
    for msg in consumer3:
        if msg.offset == last_offset - 1:
            break
