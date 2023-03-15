## "Products" microservice
*A part of "Flowers Basket" project.*

`GraphQL API`

Serves "Products" Domain.

---

#### Stack:
`Ariadne` `MongoDB` `Docker`

#### Main functionality:
- querying of Products
- mutation of Products

#### Data Models:
- Product (Bouquet | Basket )
- Flower
- Supplier

---

#### API specification:
`http://127.0.0.1:9002/voyager`

`http://127.0.0.1:9002/graphql`

`http://127.0.0.1:9002/editor`

#### API:

`http://127.0.0.1:8002`

#### Querying Products example:

```Console
{
  allProducts {
    ...on ProductInterface {
      name,
      flowers {
        flower {
          name
        },
        quantity
      }
    }
    ...on Basket {
      hasHandle
    }
    ...on Bouquet {
      hasRibbon
    }
  }
}
```

---
#### Environment variables templates:
`env/` folder

#### Run project:
```console
docker-compose up -d
```





