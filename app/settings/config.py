import logging
import os
from functools import lru_cache
from pathlib import Path
from pprint import pformat

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from settings.base import PydanticBaseSettings, BASE_DIR

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(os.environ.get("CONFIG", BASE_DIR / "config" / "config.yaml"))


class LogConfig(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter=None,
        extra="ignore",
    )

    logger_config_path: Path = BASE_DIR / "config" / "logger_config.yaml"
    path: Path = BASE_DIR / "logs"
    console_format: str = Field(
        default="%(levelname) -10s %(asctime)s %(name) -30s %(module) -30s %(funcName) -35s %(lineno) -5d: %(message)s"
    )
    file_format: str = Field(
        default="%(levelname) -10s %(asctime)s %(name) -30s %(module) -30s %(funcName) -35s %(lineno) -5d: %(message)s"
    )


class Config(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=CONFIG_PATH,
        env_nested_delimiter=None,
        extra="ignore",
    )

    log: LogConfig = LogConfig()


@lru_cache(1)
def get_config() -> Config:
    return Config()


def print_config_job(config: Config):
    for line in pformat(config.model_dump()).split("\n"):
        logger.debug(f"{line}")
