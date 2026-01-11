import logging

import glfw
import numpy as np
from OpenGL.GL import *

from settings.base import BASE_DIR
from settings.config import Config, get_config, print_config_job
from settings.logger import init_logger

logger = logging.getLogger(__name__)


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader).decode())

    return shader


def create_shader_program():
    with open(BASE_DIR / "assets/shaders/simple.vert") as f:
        VERTEX_SHADER: str = f.read()

    with open(BASE_DIR / "assets/shaders/simple.frag") as f:
        FRAGMENT_SHADER: str = f.read()

    logger.debug(f"{VERTEX_SHADER=}")
    logger.debug(f"{FRAGMENT_SHADER=}")

    vertex = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    logger.debug(f"{vertex=}")
    logger.debug(f"{fragment=}")

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program).decode())

    glDeleteShader(vertex)
    glDeleteShader(fragment)

    return program


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

    vertices = np.array(
        [0.7, -0.5, 0.0, -0.7, -0.5, 0.0, 0.0, 0.5, 0.0],
        dtype=np.float32,
    )

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    shader_program = create_shader_program()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClearColor(42 / 255, 42 / 255, 42 / 255, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    config: Config = get_config()
    init_logger(config=config)
    print_config_job(config=config)
    main()
