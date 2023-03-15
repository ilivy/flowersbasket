## "Kafka" microservice
*A part of "Flowers Basket" project.*

Runs `Apache Kafka` as a docker container.

`Apache Kafka` is an efficient messaging real time system. 

---

#### Stack:
`Apache Kafka` `Docker`

#### Main functionality:
- runs `Apache Kafka`
- provides test Producer and Consumer
- topics are autocreated

---

#### Environment variables templates:
`env/` folder

#### Run project:
```console
docker-compose up -d
```

#### Inspect 'order_created' topic:
```console
docker exec -ti kafka-ms /bin/bash
```
```console
/opt/bitnami/kafka/bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic order_created
```

#### Test Consumer:
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
