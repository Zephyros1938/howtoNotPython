from typing import Union
from OpenGL.GL import (
    glShaderSource,
    glGetProgramiv,
    glUniformMatrix4fv,
    glCreateShader,
    glCompileShader,
    glGetShaderiv,
    glGetShaderInfoLog,
    glCreateProgram,
    glAttachShader,
    glLinkProgram,
    glGetProgramInfoLog,
    glDeleteShader,
    glUseProgram,
    glDeleteProgram,
    glGetUniformLocation,
    glUniform1f,
    glUniform3f,
    glUniform1i,
    glUniform4f,
    GL_TRUE,
    GL_FALSE,
    GL_COMPILE_STATUS,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    GL_LINK_STATUS,
)
import glm


class Shader:
    def __init__(self, vertex_source: str, fragment_source: str):
        self.vertex_source = vertex_source
        self.fragment_source = fragment_source
        self.program = self._create_program(vertex_source, fragment_source)
        self._uniform_locations = {}

    def _compile_shader(self, source: str, shader_type: int) -> Union[int, None]:
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            error = glGetShaderInfoLog(shader)
            shader_type_name = {
                GL_VERTEX_SHADER: "Vertex",
                GL_FRAGMENT_SHADER: "Fragment",
            }.get(shader_type, "Unknown")
            raise RuntimeError(
                f"{shader_type_name} shader compilation error:\n{error.decode('utf-8')}"
            )
        return shader

    def _create_program(
        self, vertex_source: str, fragment_source: str
    ) -> Union[int, None]:
        vertex_shader = self._compile_shader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = self._compile_shader(fragment_source, GL_FRAGMENT_SHADER)

        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            error = glGetProgramInfoLog(program)
            raise RuntimeError(
                f"Shader program linking error:\n{error.decode('utf-8')}"
            )

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        return program

    def use(self):
        glUseProgram(self.program)

    def stop(self):
        glUseProgram(0)

    def delete(self):
        glDeleteProgram(self.program)

    def _get_uniform_location(self, name: str) -> int:
        if name not in self._uniform_locations:
            location = glGetUniformLocation(self.program, name)
            if location == -1:
                raise ValueError(f"Uniform '{name}' not found in shader")
            self._uniform_locations[name] = location
        return self._uniform_locations[name]

    # Uniform setters with GLM support
    def set_uniform1f(self, name: str, value: float):
        glUniform1f(self._get_uniform_location(name), value)

    def set_uniform1i(self, name: str, value: int):
        glUniform1i(self._get_uniform_location(name), value)

    def set_uniform_vec3(self, name: str, vec: glm.vec3):
        glUniform3f(self._get_uniform_location(name), vec.x, vec.y, vec.z)

    def set_uniform_vec4(self, name: str, vec: glm.vec4):
        glUniform4f(self._get_uniform_location(name), vec.x, vec.y, vec.z, vec.w)

    def set_uniform_mat4(self, name: str, mat: glm.mat4):
        glUniformMatrix4fv(
            self._get_uniform_location(name), 1, GL_FALSE, glm.value_ptr(mat)
        )
