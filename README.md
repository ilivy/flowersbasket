## "Flowers Basket" - Microservice Architecture demo project.

Codebase on [GitHub](https://github.com/ilivy/flowersbasket).

## Implementation

The System decomposed into microservices using 
**Domain Driven Design**, where every service:
- serves clearly differentiated area of logic
- has no strong dependencies towards other services
- owns its own data

Services communicate through the real time Messaging System (Apache Kafka).

## Microservices

* "Users" - Identity Provider (REST API) [README](https://github.com/ilivy/flowersbasket/blob/main/users_ms/README.md)
* "Products" - Products management (GraphQL) [README](https://github.com/ilivy/flowersbasket/blob/main/products_ms/README.md)
* "Orders" - Orders management (REST API) [README](https://github.com/ilivy/flowersbasket/blob/main/orders_ms/README.md)
* "Studio" - Orders processing (Web Application) [README](https://github.com/ilivy/flowersbasket/blob/main/studio_ms/README.md)
* "Kafka" - Runs Apache Kafka [README](https://github.com/ilivy/flowersbasket/blob/main/kafka_ms/README.md)

## Workflow example

#### User registration

`127.0.0.1:8001/v1/register/`

POST request: "username", "email", "password", "password_confirm"

<br/>

#### Requesting JWT token

`127.0.0.1:8001/v1/token/`

POST request with "form-data": "username", "password"

<br/>

#### Getting Products list

`127.0.0.1:8002`

POST request
```console
{
  allProducts {
    ...on ProductInterface {
      name
    }
  }
}
```

<br/>

#### Creating a new Order
`127.0.0.1:8003/v1/orders`

POST request with Order Items (including Authorization header)

<br/>

#### Schedule the Order
`127.0.0.1:8003/v1/orders/<order_id>/pay`
POST request (including Authorization header)


#### Scheduled Orders management
`127.0.0.1:8004/admin`