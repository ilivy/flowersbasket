## "Studio" microservice
*A part of "Flowers Basket" project.*

`Web application`

Serves "Studio" Domain.

## Implementation

#### Stack:
`Django` `PostreSQL` `Kafka` `Docker`

#### Main functionality:
- scheduled Orders management
- paid Orders are received for processing from `Orders` microservice using `Kafka`

#### Data Models:
- Schedule
- OrderItem
- KafkaError

#### Environment variables templates:
`env/` folder

## Usage

#### Run project:
```console
docker-compose up -d
```

#### Web application:
`127.0.0.1:8004/admin`