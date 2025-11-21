import glfw, OpenGL.GL as GL
from glm import vec3
import glm
from Std import UI
from Std.UI import imgui

from Std.ECS.Components import Camera, Transform, Velocity
import Systems
import Std


class Program:
    __contents__ = {
        "WINDOWING": {
            "width": 1920,
            "height": 1080,
            "title": "OpenGL Window",
            "MAX_FPS": -1,
            "DELTA": 0.0,
            "CLEARCOLOR": [0.1, 0.1, 0.1, 1.0],
        },
        "EXEC_KWARGS": {
            "antialias": False,
            "vsync": False,
            "debug": False,
            "fullscreen": False,
        },
        "GLFW_INIT_VALUES": {
            "context_version_major": (glfw.CONTEXT_VERSION_MAJOR, 3),
            "context_version_minor": (glfw.CONTEXT_VERSION_MINOR, 3),
            "opengl_profile": (glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE),
            "opengl_forward_compat": (glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE),
            "resizable": (glfw.RESIZABLE, GL.GL_FALSE),
            "samples": (glfw.SAMPLES, 4),
            "red_bits": (glfw.RED_BITS, 8),
            "green_bits": (glfw.GREEN_BITS, 8),
            "blue_bits": (glfw.BLUE_BITS, 8),
            "alpha_bits": (glfw.ALPHA_BITS, 8),
            "depth_bits": (glfw.DEPTH_BITS, 24),
            "stencil_bits": (glfw.STENCIL_BITS, 8),
            "doublebuffer": (glfw.DOUBLEBUFFER, GL.GL_TRUE),
            "srgb_capable": (glfw.SRGB_CAPABLE, GL.GL_TRUE),
            "transparent_framebuffer": (glfw.TRANSPARENT_FRAMEBUFFER, GL.GL_TRUE),
        },
    }

    def __preinit__(self, **kwargs):
        for key, value in kwargs.items():
            self.__contents__["EXEC_KWARGS"][key.lower()] = value
        for k, v in self.__contents__.items():
            setattr(self, k, v)

    def __init__(self, **kwargs):
        self.__preinit__(**kwargs)
        self.__initgl__(**kwargs)

        # -------------------------------
        # Example Scene Setup
        # -------------------------------
        self.scene = Std.Scene()

        # Register component types
        self.scene.registerComponentType(Transform)
        self.scene.registerComponentType(Velocity)
        self.scene.registerComponentType(Camera)

        # Create entity
        e = self.scene.createEntity()

        # Add components
        self.scene.addComponent(e, Transform(vec3(0), vec3(0), vec3(1)))
        self.scene.addComponent(e, Velocity(0, 0, 1))

        cam = self.scene.createEntity()
        self.scene.addComponent(
            cam, Camera(position=glm.vec3(0, 0, 3), yaw=-90, pitch=0)
        )

        # Add systems
        self.scene.addSystem(Systems.MovementSystem())
        self.scene.addSystem(Systems.CameraSystem())

    def __initgl__(self, **kwargs):
        if not glfw.init():
            raise Exception("GLFW initialization failed")

        for hint, (param, value) in self["GLFW_INIT_VALUES"].items():
            glfw.window_hint(param, value)

        self._window = glfw.create_window(
            self["WINDOWING"]["width"],
            self["WINDOWING"]["height"],
            self["WINDOWING"]["title"],
            glfw.get_primary_monitor() if self["EXEC_KWARGS"]["fullscreen"] else None,
            None,
        )

        if not self._window:
            glfw.terminate()
            raise Exception("GLFW window creation failed")

        glfw.make_context_current(self._window)
        if self["EXEC_KWARGS"]["vsync"]:
            glfw.swap_interval(1)
        GL.glClearColor(*self["WINDOWING"]["CLEARCOLOR"])
        imgui.create_context()
        self._impl = imgui.integrations.glfw.GlfwRenderer(self._window)
        return self

    def run(self):
        old_t = glfw.get_time()
        self.__getattribute__("WINDOWING")["DELTA"] = 0.0

        while not glfw.window_should_close(self._window):
            t = glfw.get_time()
            dt = t - old_t
            old_t = t
            self.__getattribute__("WINDOWING")["DELTA"] = dt

            glfw.poll_events()
            self._impl.process_inputs()

            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) # type: ignore

            imgui.new_frame()
            imgui.begin("Cool Window", True)
            imgui.text(f"FPS: {1 / self.__getattribute__("WINDOWING")["DELTA"]}")
            imgui.end()

            # Update non-UI ECS systems
            self.scene.update(dt)

            # -------------------------------------------------
            # Render ImGui AFTER systems finish drawing
            # -------------------------------------------------
            UI.renderImGuiData(self._impl)

            glfw.swap_buffers(self._window)

        glfw.terminate()
        return self

    def cleanup(self):
        pass

    def __setitem__(self, key, item):
        self.__contents__[key] = item

    def __getitem__(self, key):
        return self.__contents__[key]


# ==================================================================
# MAIN ENTRY
# ==================================================================


def parse_args(argv):
    def parseArgValue(value: str):
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        return value

    result = {}
    for arg in argv:
        if "=" in arg:
            key, value = arg.split("=", 1)
            # Strip optional surrounding quotes
            value = value.strip('"').strip("'")
            result[key] = parseArgValue(value)
    return result


if __name__ == "__main__":
    Program(**parse_args(__import__("sys").argv[1:])).run().cleanup()
