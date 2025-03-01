# This sample serves several purposes:
# * Demonstrate a slightly different code style from most Panda3D
#   examples.
# * Give people new to Panda3D a way to dive right into basic shader
#   development.
# * Help people used to shadertoy.com an easier way to transition to
#   Panda3D. (Note: This is NOT a drop-in replacement for shadertoy.)
# * Sneaking it past rdb that I'm actually just dropping a cool toy into
#   the samples folder.
#
# What it does is:
# * Cover the window in a quad and apply a shader to it.
# * Monitor the shader source files, and update the shader when they are
#   updated.
# * Provide some hotkeys:
#   `f`: Toggle fullscreen mode and hide the mouse while in it.
#   `r`: Restart time (or rather the task generating the shader inputs).
#   `escape`: Exit pandatoy.
#
# How to use pandatoy:
# * By default, the files `pandatoy.vert` and `pandatoy.frag` are used
#   to shade the quad.
# * `pandatoy.frag`, the fragment shader, is the file you'd typically
#   play around with.
# * Other files can be used by specifying them on the command line, e.g.
#   `python main.py --fragment pretty_circles.frag`
#
# What GLSL variables pandatoy provides:
# * Panda3D's suite of automatic inputs
#   https://docs.panda3d.org/1.10/python/programming/shaders/list-of-glsl-inputs
# * `float iTime` / `float time`: Time since the (last re-)start.
# * `float iTimeDelta` / `float dt`: Render time of the last frame.
# * `int iFrame` / `int frame`: Number of the current frame since the
#   (last re-)start.
# * `vec2 aspect`: The aspect ratio of the window, using Panda3D's
#   format; The shorter axis has a value of 1, the longer one an
#   accordingly higher one.


import argparse
import os

from direct.showbase.ShowBase import ShowBase

from panda3d.core import CardMaker
from panda3d.core import Shader
from panda3d.core import Vec2
from panda3d.core import Vec3
from panda3d.core import WindowProperties


# One big advantage of Panda3D over some engines is that you have full
# access to all of Python's ecosystem of tools and libraries.
parser = argparse.ArgumentParser(
    description="Displays your shader on a window-filling quad. Press `f` to toggle fullscreen, `escape` to quit.",
)
parser.add_argument(
    '-v',
    '--vertex',
    type=str,
    default='pandatoy.vert',
    help="File name of vertex shader to use.",
)
parser.add_argument(
    '-f',
    '--fragment',
    type=str,
    default='pandatoy.frag',
    help="File name of fragment shader to use.",
)
args = parser.parse_args()


# Most of Panda3D's samples and tutorials make their application class
# inherit `ShowBase`. While not inherently harmful, it is also
# unnecessary, and frankly inelegant, as it mixes up the game engine
# with the game itself. In my not so humble opinion, accessing the
# `ShowBase` instance via `base`, the builtin created when `ShowBase` is
# instanced, leads to more elegant source code, and defers the need to
# use object orientation.
ShowBase()
base.accept('escape', base.task_mgr.stop)
base.disableMouse()


# In this specific case though, that deferment does not last long.
class Manager:
    def __init__(self, vertex_shader_file, fragment_shader_file):
        self.shader_files = dict(
            vertex=vertex_shader_file,
            fragment=fragment_shader_file,
        )

        card_maker = CardMaker('card')
        card_maker.set_frame(-1, 1, -1, 1)
        self.card = base.render2d.attach_new_node(card_maker.generate())
        self.load_shader()

        self.file_times = {fn: os.path.getmtime(fn) for fn in self.shader_files.values()}
        base.task_mgr.add(self.check_for_file_updates, sort=5)
        base.task_mgr.add(self.update_shader_inputs, "Update shader inputs", sort=10)
        base.accept('r', self.restart_shader_inputs)

        base.accept('f', self.toggle_fullscreen)

    def check_for_file_updates(self, task):
        update = False
        for fn in self.file_times:
            new_time = os.path.getmtime(fn)
            if new_time > self.file_times[fn]:
                update = True
            self.file_times[fn] = new_time
        if update:
            print("Reloading shaders...", end="")
            self.load_shader()
            print("Done.")
        return task.cont

    def load_shader(self):
        shader = Shader.load(
            Shader.SL_GLSL,
            **self.shader_files,
        )
        self.card.set_shader(shader)

    def update_shader_inputs(self, task):
        res = base.win.get_properties().size
        extended_res = Vec3(res.x, res.y, res.x/res.y)
        # Shadertoy compatibility inputs
        self.card.set_shader_input('iTime', task.time)
        self.card.set_shader_input('iTimeDelta', globalClock.dt)
        self.card.set_shader_input('iFrame', task.frame)
        self.card.set_shader_input('iResolution', extended_res)

        # Equivalent and additional inputs
        self.card.set_shader_input('time', task.time)
        self.card.set_shader_input('dt', globalClock.dt)
        self.card.set_shader_input('frame', task.frame)
        self.card.set_shader_input('resolution', res)
        self.card.set_shader_input('aspectRatio', extended_res.z)
        top_right = base.a2dTopRight.get_pos()
        self.card.set_shader_input('aspect', Vec2(top_right.x, top_right.z))
        return task.cont

    def restart_shader_inputs(self):
        base.task_mgr.remove("Update shader inputs")
        self.shader_input_task = base.task_mgr.add(self.update_shader_inputs, "Update shader inputs", sort=10)

    def toggle_fullscreen(self):
        wp = WindowProperties(base.win.get_properties())
        wp.fullscreen = not wp.fullscreen
        wp.cursor_hidden = not wp.cursor_hidden
        base.win.requestProperties(wp)


Manager(args.vertex, args.fragment)
base.run()
