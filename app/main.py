import logging

import glfw

from settings.config import Config, get_config, print_config_job
from settings.logger import init_logger


logger = logging.getLogger(__name__)


def main():
    logger.info("Hello from adventure!")

    if not glfw.init():
        raise RuntimeError("Can't glfw.init")

    window = glfw.create_window(
        640,
        480,
        "Adventures game",
        None,
        None,
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Can't glfw.create_window")

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    config: Config = get_config()
    init_logger(config=config)
    print_config_job(config=config)
    main()
