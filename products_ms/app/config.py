import logging
import os

from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, MongoDsn

logger = logging.getLogger(__name__)


class EnvironmentEnum(str, Enum):
    DEV = "dev"
    PROD = "prod"


class GlobalConfig(BaseSettings):
    TITLE: str = "Flowers Basket - Products"
    DESCRIPTION: str = "Products microservice"

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TIMEZONE: str = "UTC"

    DATABASE_DSN: Optional[MongoDsn] = "mongodb+srv://username:pwd@mongohost:27017"
    DB_ECHO_LOG: bool = False

    API_V1_STR: str = "/v1"

    @property
    def srv_database_dsn(self) -> Optional[str]:
        return (
            self.DATABASE_DSN.replace("mongodb://", "mongodb+srv://")
            if self.DATABASE_DSN
            else self.DATABASE_DSN
        )

    class Config:
        case_sensitive = True


class DevConfig(GlobalConfig):
    """Dev configuration."""

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV


class ProdConfig(GlobalConfig):
    """Prod configuration."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PROD


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        if self.environment == EnvironmentEnum.DEV.value:
            return DevConfig()
        return ProdConfig()


@lru_cache()
def get_configuration() -> GlobalConfig:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
