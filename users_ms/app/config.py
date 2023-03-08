import logging
import os
from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, PostgresDsn

logger = logging.getLogger(__name__)


class EnvironmentEnum(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class GlobalConfig(BaseSettings):
    TITLE: str = "FlowersBasketUsers"
    DESCRIPTION: str = "Users microservice"

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TIMEZONE: str = "UTC"

    JWT_SECRET: str = "jwtsecret"

    DATABASE_DSN: Optional[
        PostgresDsn
    ] = "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
    DB_ECHO_LOG: bool = False

    @property
    def psycopg2_database_dsn(self) -> Optional[str]:
        return (
            self.DATABASE_DSN.replace("postgresql://", "postgresql+psycopg2://")
            if self.DATABASE_DSN
            else self.DATABASE_DSN
        )

    API_V1_STR: str = "/v1"

    class Config:
        case_sensitive = True


class DevConfig(GlobalConfig):
    """Dev configuration."""

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV


class TestConfig(GlobalConfig):
    """Test configurations."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.TEST

    @property
    def psycopg2_database_dsn(self) -> Optional[str]:
        # adds "_test" to DB name, if "DATABASE_DSN" is set
        parent_db_dsn = GlobalConfig.psycopg2_database_dsn.fget(self)
        return parent_db_dsn and parent_db_dsn + "_test"


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
        if self.environment == EnvironmentEnum.TEST.value:
            return TestConfig()
        return ProdConfig()


@lru_cache()
def get_configuration() -> GlobalConfig:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
