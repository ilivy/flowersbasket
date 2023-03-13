## "Orders" microservice

A part of "Flowers Basket" project
### Run project
`docker-compose up -d`

### Run tests
`docker-compose exec -e ENVIRONMENT=test orders-api pytest`


### Generate migrations
`docker-compose exec orders-api alembic revision --autogenerate -m "Updating db"`

### Run migrations
`docker-compose exec orders-api alembic upgrade head`
