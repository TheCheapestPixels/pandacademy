from panda3d.core import WindowProperties
from panda3d.core import TextNode

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase


ShowBase()
base.accept('escape', base.task_mgr.stop)
current_state_text = OnscreenText(
    text="",
    parent=base.a2dTopLeft,
    align=TextNode.ALeft,
    pos=(0.01, -0.1),
    scale=0.1,
)


def inspection_loop(task):
    props = base.win.get_properties()
    # You can simply print the object to see most data. Let's do that if
    # the window is hidden. Fun fact: On my system, this doesn't work,
    # the window says it isn't minimized even when it is.
    if props.minimized:
        print(props)
    else:
        status = f"Title: {props.title}\n"
        status += f"Undecorated: {props.undecorated}\n"
        status += f"Icon filename: {props.icon_filename}\n"
        status += f"\n"
        status += f"Open: {props.open}\n"
        status += f"Minimized: {props.minimized}\n"
        status += f"Fullscreen: {props.fullscreen}\n"
        status += f"Fixed size: {props.fixed_size}\n"
        status += f"Size: {props.size}\n"
        status += "\n"
        status += f"Cursor hidden: {props.cursor_hidden}\n"
        status += f"Cursor filename: {props.cursor_filename}\n"
        mm_to_str = {
            WindowProperties.M_absolute: "WindowProperties.M_absolute",
            WindowProperties.M_relative: "WindowProperties.M_relative",
            WindowProperties.M_confined: "WindowProperties.M_confined",
        }
        status += f"Mouse Mode: {mm_to_str[props.mouse_mode]}\n"
        status += "\n"
        status += f"Origin: {props.origin}\n"
        status += f"Foreground: {props.foreground}\n"
        status += f"Parent Window: {props.parent_window}\n"
        zo_to_str = {
            WindowProperties.Z_bottom: "WindowProperties.Z_bottom",
            WindowProperties.Z_top: "WindowProperties.Z_top",
            WindowProperties.Z_normal: "WindowProperties.Z_normal",
        }
        status += f"Z Order: {props.z_order}\n"
        current_state_text['text'] = status
    return task.cont


base.task_mgr.add(inspection_loop)
base.run()
