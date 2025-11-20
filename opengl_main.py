from typing import Any
import glfw, glm, OpenGL.GL as GL


class Program:
    __contents__ = {
        "WINDOWING": {
            "width": 1920,
            "height": 1080,
            "title": "OpenGL Window",
            "MAX_FPS": 60,
            "DELTA": 0.0,
            "CLEARCOLOR": [0.1, 0.1, 0.1, 0.5],
        },
        "EXEC_KWARGS": {
            "antialias": True,
            "vsync": True,
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
            "transparent_framebuffer": (glfw.TRANSPARENT_FRAMEBUFFER, GL.GL_TRUE)
        },
    }

    def __preinit__(self, **kwargs):
        for k, v in self.__contents__.items():
            setattr(self, k, v)
        for key, value in kwargs.items():
            self.__contents__["EXEC_KWARGS"][key.lower()] = value

    def __init__(self, **kwargs):
        self.__preinit__(**kwargs)
        self.__initgl__(**kwargs)
        print(__import__("json").dumps(self.WINDOWING, indent=4))

        # gutted asset manager placeholder
        self["AssetManager"] = AssetManager()
        AM = self["AssetManager"]

        # placeholder registration
        AM.registerImage("home", "home")

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
        return self

    def run(self):
        while not glfw.window_should_close(self._window):
            glfw.poll_events()
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            glfw.swap_buffers(self._window)
        glfw.terminate()

        return self

    def cleanup(self):
        pass

    def initializeAttributesS1(self, codeToDo: list[str] = []):
        for x in codeToDo:
            exec(x, globals(), locals())
        return self

    def initializeAttributesS2(self, **classes):
        for name, cls in classes.items():
            setattr(Program, name, cls)
        return self

    def __setitem__(self, key, item):
        self.__contents__[key] = item

    def __getitem__(self, key):
        return self.__contents__[key]


# ==================================================================
# GUTTED ASSET MANAGER
# ==================================================================


class AssetManager:
    def __init__(self):
        self._assets = {}

    def registerImage(self, name, obj):
        self._assets[name] = PlaceholderImage(name)

    def getImage(self, name):
        if name not in self._assets:
            raise Exception(f"Image not registered: {name}")
        return self._assets[name]


# ==================================================================
# PLACEHOLDER IMAGE OBJECT
# ==================================================================


class PlaceholderImage:
    def __init__(self, name):
        self.name = name


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
    Program(
        **parse_args(__import__("sys").argv[1:])
    ).initializeAttributesS1().initializeAttributesS2().run().cleanup()
