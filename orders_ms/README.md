## "Orders" microservice
*A part of "Flowers Basket" project.*

`REST API`

Serves "Orders" Domain.

## Implementation

#### Stack:
`FastAPI` `PostreSQL` `Kafka` `Docker`

#### Main functionality:
- CRUD operations with Orders
- paid Orders are sent for processing into `Studio` microservice using `Kafka`

#### Data Models:
- Order
- OrderItem

#### Environment variables templates:
`env/` folder

## Usage

#### Run project:
```console
docker-compose up -d
```

#### Run tests:
```console
docker-compose exec -e ENVIRONMENT=test orders-api pytest
```

#### Generate migrations:
```console
docker-compose exec orders-api alembic revision --autogenerate -m "Updating db"
```

#### Run migrations:
```console
docker-compose exec orders-api alembic upgrade head
```

#### API specification:
`127.0.0.1:8003/docs`
