## "Kafka" microservice

A part of "Flowers Basket" project.
Runs Apache Kafka as a docker container.

Topics are autocreated.

Docker external network `kafkantw` can be used in other networks for communication with Kafka.

Service `kafka:9092`

### Run project
`docker-compose up -d`

### Inspect 'order_created' topics
`docker exec -ti kafka-ms /bin/bash`
```console
/opt/bitnami/kafka/bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic order_created
```

### Test Consumer
```console
pipenv install
pipenv shell
python consumer.py
```

### Test Producer
```console
pipenv install
pipenv shell
python producer.py
```
