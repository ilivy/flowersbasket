from pymongo import MongoClient

from app.config import settings


def get_database():
    client = MongoClient(settings.DATABASE_DSN)
    return client["fb_products"]
