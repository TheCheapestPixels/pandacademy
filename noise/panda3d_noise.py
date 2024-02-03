from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import ComputeNode
from panda3d.core import Shader
from panda3d.core import ShaderAttrib
from panda3d.core import CardMaker
from panda3d.core import PfmFile
from panda3d.core import TextureStage
from panda3d.core import Texture
from panda3d.core import LColor

from direct.showbase.ShowBase import ShowBase


resolution = 512
image = PfmFile()
image.clear(
    x_size=resolution,
    y_size=resolution,
    num_channels=4,
)
image.fill(Vec4(1, 0, 0, 1))
texture = Texture('')
texture.setup_2d_texture(
    image.get_x_size(),
    image.get_y_size(),
    Texture.T_float,
    Texture.F_rgba32,
)
texture.load(image)


ShowBase()
base.cam.set_pos(0.5, -2.0, 0.5)
base.accept('escape', base.task_mgr.stop)


card = render.attach_new_node(CardMaker('card').generate())
card.set_texture(texture)
cn = ComputeNode("compute noise")
cn.add_dispatch(resolution // 16, resolution // 16, 1)
np = card.attach_new_node(cn)
#shader = Shader.load_compute(Shader.SL_GLSL, "psrd_single_layer.glsl")
#shader = Shader.load_compute(Shader.SL_GLSL, "psrd_multi_layer.glsl")
#shader = Shader.load_compute(Shader.SL_GLSL, "perlin_single_layer.glsl")
shader = Shader.load_compute(Shader.SL_GLSL, "worley_single_layer.glsl")
np.set_shader(shader)
np.set_shader_input("tex", texture)
def update_shader_time(task):
    np.set_shader_input("time", task.time)
    return task.cont
base.task_mgr.add(update_shader_time)


base.run()
