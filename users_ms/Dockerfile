FROM python:3.10

RUN mkdir -p /microservice/app

WORKDIR /microservice

RUN apt-get -y update \
    && apt-get -y upgrade \
    && pip install --upgrade pip setuptools wheel \
    && pip install pipenv

COPY Pipfile Pipfile.lock /microservice/
RUN pipenv install --system --deploy

ENV PYTHONPATH=.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY alembic.ini .
COPY pytest.ini .

COPY ./app ./app
COPY ./migrations ./migrations
COPY ./tests ./tests

EXPOSE 8001

ENV ENVIRONMENT="dev"
ENV DATABASE_DSN="postgresql://postgres:postgres@postgres:5432/postgres"
ENV JWT_SECRET="secret"

CMD ["uvicorn", "app.web.main:app", "--host", "0.0.0.0", "--reload"]
