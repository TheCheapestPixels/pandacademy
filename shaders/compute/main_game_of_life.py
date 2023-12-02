# In `main_basic_compute.py` I started out by motivating the use of
# compute shaders by talking about the raw computing power that it
# brings to the table, 

import random

import jinja2

from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Shader
from panda3d.core import ComputeNode
from panda3d.core import ShaderAttrib
from panda3d.core import CardMaker
from panda3d.core import PNMImage
from panda3d.core import PfmFile
from panda3d.core import TextureStage
from panda3d.core import Texture

from direct.showbase.ShowBase import ShowBase


shader_template = """#version 430

layout (local_size_x = {{workgroup_size}}, local_size_y = {{workgroup_size}}) in;

layout(rgba32f) uniform image2D fromTex;
layout(rgba32f) uniform writeonly image2D toTex;

ivec2 bottomLeft   = ivec2(-1, -1);
ivec2 bottomMiddle = ivec2( 0, -1);
ivec2 bottomRight  = ivec2( 1, -1);
ivec2 middleLeft   = ivec2(-1,  0);
ivec2 middleRight  = ivec2( 1,  0);
ivec2 topLeft      = ivec2(-1,  1);
ivec2 topMiddle    = ivec2( 0,  1);
ivec2 topRight     = ivec2( 1,  1);

ivec2 donutCoord(ivec2 coord) {
    ivec2 imgSize = imageSize(fromTex);
    int x = int(mod(coord.x, imgSize.x));
    int y = int(mod(coord.y, imgSize.y));
    return ivec2(x, y);
}

void main() {
  ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
  vec4 myself = imageLoad(fromTex, coord);
  vec4 neighbors = imageLoad(fromTex, donutCoord(coord + bottomLeft)) +
                   imageLoad(fromTex, donutCoord(coord + bottomMiddle)) +
                   imageLoad(fromTex, donutCoord(coord + bottomRight)) +
                   imageLoad(fromTex, donutCoord(coord + middleLeft)) +
                   imageLoad(fromTex, donutCoord(coord + middleRight)) +
                   imageLoad(fromTex, donutCoord(coord + topLeft)) +
                   imageLoad(fromTex, donutCoord(coord + topMiddle)) +
                   imageLoad(fromTex, donutCoord(coord + topRight));
  float new_state;
  if (myself.r == 1.0) {  // Cell is alive
    if ((2.0 <= neighbors.r) && (neighbors.r <= 3.0)) {
      new_state = 1.0;  // 2 or 3 live neighbors, survives
    } else {
      new_state = 0.0;  // 1 or more than 3 live neighbors, dies
    }
  } else {  // Cell is dead
    if (neighbors.r == 3.0) {
      new_state = 1.0;
    } else {
      new_state = 0.0;
    }
  }
  
  vec4 new_cell = vec4(new_state, 0, 0, 1);
  // vec4 new_cell = vec4(myself.r, 0, 0, 1);
  imageStore(toTex, coord, new_cell);
  memoryBarrierImage();
  imageStore(fromTex, coord, new_cell);
}
"""


class GameOfLife:
    def __init__(self, resolution=64, workgroup_size=16):
        self.resolution = resolution
        self.workgroup_size = workgroup_size
        self.image_in, self.texture_in = self.make_texture(random_noise=False)
        self.image_out, self.texture_out = self.make_texture()
        self.setup_shader()

    def make_texture(self, random_noise=False):
        image = PfmFile()
        image.clear(
            x_size=self.resolution,
            y_size=self.resolution,
            num_channels=4,
        )
        if not random_noise:
            image.fill(Vec4(0, 0, 0, 1))
            image.set_point(20, 20, 1)
            image.set_point(21, 20, 1)
            image.set_point(22, 20, 1)
            image.set_point(22, 19, 1)
            image.set_point(21, 18, 1)
        else:
            for x in range(self.resolution):
                for y in range(self.resolution):
                    image.set_point(x, y, random.randint(0, 1))
        texture = Texture('')
        texture.setup_2d_texture(
            image.get_x_size(),
            image.get_y_size(),
            Texture.T_float,
            Texture.F_rgba32,
        )
        texture.load(image)
        from panda3d.core import SamplerState
        texture.set_magfilter(SamplerState.FT_nearest)
        return (image, texture)

    def setup_shader(self):
        environment = jinja2.Environment()
        template = environment.from_string(shader_template)
        shader_source = template.render(workgroup_size=self.workgroup_size)
        for idx, line in enumerate(shader_source.split('\n')):
            print(f"{idx:03} {line}")
        self.shader = Shader.make_compute(
            Shader.SL_GLSL,
            shader_source,
        )
        node = ComputeNode("compute")
        workgroups = (
            self.resolution // self.workgroup_size,
            self.resolution // self.workgroup_size,
            1,
        )
        node.add_dispatch(*workgroups)
        compute_np = NodePath(node)
        compute_np.set_shader(self.shader)
        compute_np.set_shader_input("fromTex", self.texture_in)
        compute_np.set_shader_input("toTex", self.texture_out)
        self.compute_np = compute_np

    def shade(self, nodepath):
        self.nodepath = nodepath
        nodepath.set_texture(self.texture_in)
        self.compute_np.reparent_to(nodepath)


ShowBase()
base.cam.set_pos(0.5, -2.0, 0.5)
base.accept('escape', base.task_mgr.stop)
base.set_frame_rate_meter(True)

game_of_life = GameOfLife(resolution=128)
cm = CardMaker('card')
card = render.attach_new_node(cm.generate())
game_of_life.shade(card)

base.run()
