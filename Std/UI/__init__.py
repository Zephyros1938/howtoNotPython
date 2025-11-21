
from typing import Any
import imgui as _imgui
from imgui.integrations.glfw import GlfwRenderer

_imgui: Any
imgui = _imgui

def renderImGuiData(impl: imgui.integrations.glfw.GlfwRenderer):
    imgui.render()
    impl.render(imgui.get_draw_data())