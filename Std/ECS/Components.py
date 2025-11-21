from dataclasses import dataclass

from glm import vec3
import glm

from Std.ECS import Component


@dataclass
class Transform(Component):
    position: vec3 = vec3(0)
    rotation: vec3 = vec3(0)
    scale: vec3 = vec3(0)

@dataclass
class Velocity(Component):
    x: float = 0
    y: float = 0
    z: float = 0

@dataclass
class Camera(Component):
    position: glm.vec3 = glm.vec3(0.0, 0.0, 3.0)
    yaw: float = -90.0
    pitch: float = 0.0
    fov: float = 45.0
    near: float = 0.1
    far: float = 100.0

    # Internal matrices (updated each frame)
    view: glm.mat4 = glm.mat4(1.0)
    projection: glm.mat4 = glm.mat4(1.0)
