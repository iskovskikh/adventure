import logging
import logging.config

from jinja2 import Template

from yaml import safe_load

from settings.config import Config


def get_logger_config(config: Config):
    config.log.path.mkdir(parents=True, exist_ok=True)

    with open(config.log.logger_config_path) as file:
        raw_yaml_str: str = file.read()

    rendered_str: str = Template(raw_yaml_str).render(config=config)

    return safe_load(rendered_str)


def init_logger(config: Config):
    logging.config.dictConfig(get_logger_config(config=config))
    logging.info("Init logger")
