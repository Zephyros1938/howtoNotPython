import glm
from Std import Scene
from Std.ECS import System
from Std.ECS.Components import Camera, Transform, Velocity


class MovementSystem(System):
    required = (Transform, Velocity)

    def run(self, scene: Scene, dt: float):
        pos_storage = scene.storage(Transform)
        vel_storage = scene.storage(Velocity)

        for entity in pos_storage.data.keys():
            if vel_storage.has(entity):
                p: Transform = pos_storage.get(entity)
                v: Velocity = vel_storage.get(entity)
                p.position.x += v.x * dt
                p.position.y += v.y * dt
                p.position.z += v.z * dt

class CameraSystem(System):
    required = (Camera,)

    def run(self, scene: Scene, dt: float):
        cam_storage = scene.storage(Camera)
        width = 1920   # You may link these to Program.WINDOWING
        height = 1080
        aspect = width / height

        for entity, cam in cam_storage.data.items():

            # Convert angles to radians
            yaw_r = glm.radians(cam.yaw)
            pitch_r = glm.radians(cam.pitch)

            # Compute forward direction
            front = glm.vec3(
                glm.cos(yaw_r) * glm.cos(pitch_r),
                glm.sin(pitch_r),
                glm.sin(yaw_r) * glm.cos(pitch_r)
            )
            front = glm.normalize(front)

            # Compute view matrix
            cam.view = glm.lookAt(
                cam.position,
                cam.position + front,
                glm.vec3(0.0, 1.0, 0.0)
            )

            # Compute projection matrix
            cam.projection = glm.perspective(
                glm.radians(cam.fov),
                aspect,
                cam.near,
                cam.far
            )

class UISystem(System):
    required = ()

    def run(self, scene: Scene, dt: float):
        pass