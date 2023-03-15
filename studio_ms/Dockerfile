FROM python:3.10

RUN mkdir -p /microservice/studio

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

COPY ./studio ./studio

#EXPOSE 8004

ENV ENVIRONMENT="dev"
ENV DATABASE_DSN="postgresql://postgres:postgres@postgres:5432/postgres"

#CMD ["python", "studio/manage.py", "runserver", "0.0.0.0:8000"]
