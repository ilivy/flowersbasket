## "Users" microservice
*A part of "Flowers Basket" project.*

`REST API`

Serves "Users" Domain.

---

#### Stack:
`FastAPI` `PostreSQL` `Docker`

#### Main functionality:
- registers new Users
- acts as Identity Provider (`OAuth2` "password flow" security schema)

#### Data Models:
- User

---

#### API specification:
`127.0.0.1:8001/docs`

#### Requesting JWT:
`127.0.0.1:8001/v1/token/`

expects  "form data" with "username" and "password"

---

#### Environment variables templates:
`env/` folder

#### Run project:
```console
docker-compose up -d
```

#### Run tests:
```console
docker-compose exec -e ENVIRONMENT=test users-api pytest
```

#### Generate migrations:
```console
docker-compose exec users-api alembic revision --autogenerate -m "Updating db"
```

#### Run migrations:
```console
docker-compose exec users-api alembic upgrade head 
```