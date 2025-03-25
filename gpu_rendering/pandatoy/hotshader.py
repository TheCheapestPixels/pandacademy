import os

from panda3d.core import Shader


class HotShader:
    def __init__(self, nodepath, vertex=None, fragment=None):
        assert (vertex is not None) and (fragment is not None), "HotShader requires a vertex *and* a fragment shader."
        self.nodepath = nodepath
        self.shader_files = dict(
            vertex=vertex,
            fragment=fragment,
        )
        self.file_times = {fn: os.path.getmtime(fn) for fn in self.shader_files.values()}
        base.task_mgr.add(self.check_for_file_updates, sort=5)
        self.load_shader()

    def load_shader(self):
        shader = Shader.load(
            Shader.SL_GLSL,
            **self.shader_files,
        )
        self.nodepath.set_shader(shader)

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
