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

COPY ./app ./app

EXPOSE 8002

ENV ENVIRONMENT="dev"
ENV DATABASE_DSN="mongodb://mongouser:mongopass@localhost:27017"

CMD ["uvicorn", "app.web.main:server", "--host", "0.0.0.0", "--reload"]