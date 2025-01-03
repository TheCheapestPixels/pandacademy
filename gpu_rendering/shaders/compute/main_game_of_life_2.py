# This is the basic Game of Life code all over, except for one important
# change in the compute shader; That is why all commentary besides this
# one is in the shader code.
#
# Right now, we are doing nine `imageLoad`s per texel. Memory bandwidth
# is a limited resource though, so let's try to use it sparingly. Can we
# do better than nine loads? Well, the answer is obviously "Yes", so let
# me explain...
#
# All of a workgroup's invocations run on the same compute unit on the
# GPU. These units also have a bit of memory which the invocations can
# share. That means that if we load the relevant tile into that shared
# memory, and use it as the basis for our calculations, then we have
# much fewer `imageLoad`s to do; With a 16x16x1 workgroup, we need an
# 18x18 tile, yielding 324 loads instead of 2304, resulting in just 14%
# the memory bandwidth used in this step. So let's do it.


import random
from enum import Enum

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


class Pattern(Enum):
    BLANK = 0
    RANDOM = 1
    SPINNER = 2
    GLIDER = 3
    PENTOMINO = 4


shader_source = """#version 430

layout (local_size_x = 16, local_size_y = 16) in;

layout(rgba32f) uniform image2D fromTex;
layout(rgba32f) uniform writeonly image2D toTex;

// This time we are sharing a variable between all invocations in a
// workgroup
shared float tile[18][18];

ivec2 bottomLeft   = ivec2(-1, -1);
ivec2 bottomMiddle = ivec2( 0, -1);
ivec2 bottomRight  = ivec2( 1, -1);
ivec2 middleLeft   = ivec2(-1,  0);
ivec2 middleRight  = ivec2( 1,  0);
ivec2 topLeft      = ivec2(-1,  1);
ivec2 topMiddle    = ivec2( 0,  1);
ivec2 topRight     = ivec2( 1,  1);

// Mapping arbitrary coords to the texture, gluing the edges together.
ivec2 donutCoord(ivec2 coord) {
    ivec2 imgSize = imageSize(fromTex);
    int x = int(mod(coord.x, imgSize.x));
    int y = int(mod(coord.y, imgSize.y));
    return ivec2(x, y);
}

void preloadTile(image2D tex) {
  ivec2 tileCoord = ivec2(gl_LocalInvocationID.xy) + ivec2(1, 1);
  ivec2 imgCoord = ivec2(gl_GlobalInvocationID.xy);
  // First, let's load this invocation's texel; That's trivial.
  tile[tileCoord.x][tileCoord.y] = imageLoad(tex, imgCoord).r;
  // If the texel is on the left / right edge, we load the fringe texel
  // as well.
  if (tileCoord.x == 1) {
    tile[0][tileCoord.y] = imageLoad(tex, donutCoord(imgCoord + middleLeft)).r;
    // Here at the border we also check whether we are at a corner, in
    // which case we load the fringe corner, too.
    if (tileCoord.y == 1) {
      tile[0][0] = imageLoad(tex, donutCoord(imgCoord + bottomLeft)).r;
    } else if (tileCoord.y == gl_WorkGroupSize.y) {
      tile[0][tileCoord.y + 1] = imageLoad(tex, donutCoord(imgCoord + topLeft)).r;
    }
  } else if (tileCoord.x == gl_WorkGroupSize.x) {
    // Same as above, just at the opposite edge / corners.
    tile[tileCoord.x + 1][tileCoord.y] = imageLoad(tex, donutCoord(imgCoord + middleRight)).r;
    if (tileCoord.y == 1) {
      tile[tileCoord.x + 1][0] = imageLoad(tex, donutCoord(imgCoord + bottomRight)).r;
    } else if (tileCoord.y == gl_WorkGroupSize.y) {
      tile[tileCoord.x + 1][tileCoord.y + 1] = imageLoad(tex, donutCoord(imgCoord + topRight)).r;
    }
  }
  // Now the other edge. Here we only have to care about the edge of the
  // fringe, not the corners, because those have been dealt with above
  // already.
  if (tileCoord.y == 1) {
    tile[tileCoord.x][0] = imageLoad(tex, donutCoord(imgCoord + bottomMiddle)).r;
  } else if (tileCoord.y == gl_WorkGroupSize.y) {
    tile[tileCoord.x][tileCoord.y + 1] = imageLoad(tex, donutCoord(imgCoord + topMiddle)).r;
  }
  // And now we need to synchronize the invocations in ths workgroup.
  barrier();
}

float fetchTile(ivec2 coord) {
  int tileX = coord.x + 1;
  int tileY = coord.y + 1;
  return tile[tileX][tileY];
}

void main() {
  preloadTile(fromTex);
  // We'll need to work in tile space now, so let's not forget the
  // offset.
  ivec2 coord = ivec2(gl_LocalInvocationID.xy);
  bool amAlive = fetchTile(coord) == 1.0;
  // ...and how many neighbors are?
  float neighs = fetchTile(coord + bottomLeft) +
                 fetchTile(coord + bottomMiddle) +
                 fetchTile(coord + bottomRight) +
                 fetchTile(coord + middleLeft) +
                 fetchTile(coord + middleRight) +
                 fetchTile(coord + topLeft) +
                 fetchTile(coord + topMiddle) +
                 fetchTile(coord + topRight);
  int livNeighs = int(neighs);

  bool willBeAlive = (amAlive && livNeighs==2) || (livNeighs==3);
  imageStore(toTex, ivec2(gl_GlobalInvocationID.xy), vec4(willBeAlive, 0., 0., 1.));
}
"""


class GameOfLife:
    def __init__(self, resolution=64, pattern=Pattern.RANDOM):
        self.resolution = resolution
        self.image_in, self.texture_in = self.make_texture(Pattern.BLANK)
        self.image_out, self.texture_out = self.make_texture(pattern)
        self.setup_shader()

    def make_texture(self, pattern):
        image = PfmFile()
        image.clear(
            x_size=self.resolution,
            y_size=self.resolution,
            num_channels=4,
        )
        image.fill(Vec4(0, 0, 0, 1))
        offset = self.resolution // 2
        if pattern == Pattern.BLANK:
            pass
        elif pattern == Pattern.SPINNER:
            image.set_point(offset - 1, offset, 1)
            image.set_point(offset    , offset, 1)
            image.set_point(offset + 1, offset, 1)
        elif pattern == Pattern.GLIDER:
            image.set_point(offset - 1, offset    , 1)
            image.set_point(offset    , offset + 1, 1)
            image.set_point(offset + 1, offset - 1, 1)
            image.set_point(offset + 1, offset    , 1)
            image.set_point(offset + 1, offset + 1, 1)
        elif pattern == Pattern.PENTOMINO:
            image.set_point(offset - 1, offset    , 1)
            image.set_point(offset - 1, offset + 1, 1)
            image.set_point(offset    , offset - 1, 1)
            image.set_point(offset    , offset    , 1)
            image.set_point(offset + 1, offset    , 1)
        else:  # Pattern.RANDOM
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
        for idx, line in enumerate(shader_source.split('\n')):
            print(f"{idx:03} {line}")
        self.shader = Shader.make_compute(
            Shader.SL_GLSL,
            shader_source,
        )
        node = ComputeNode("compute")
        node.add_dispatch(16, 16, 1)
        compute_np = NodePath(node)
        compute_np.set_shader(self.shader)
        compute_np.set_shader_input("fromTex", self.texture_in)
        compute_np.set_shader_input("toTex", self.texture_out)
        self.compute_np = compute_np

    def shade(self, nodepath, swap_tex_at=0):
        self.nodepath = nodepath
        nodepath.set_texture(self.texture_in)
        self.compute_np.reparent_to(nodepath)
        base.task_mgr.add(self.swap_textures, sort=swap_tex_at)

    def swap_textures(self, task):
        old_tex_in = self.texture_in
        old_tex_out = self.texture_out
        self.texture_in = old_tex_out
        self.texture_out = old_tex_in
        self.compute_np.set_shader_input("fromTex", self.texture_in)
        self.compute_np.set_shader_input("toTex", self.texture_out)
        self.nodepath.set_texture(self.texture_in)
        return task.cont


ShowBase()
base.cam.set_pos(0.5, -2.0, 0.5)
base.accept('escape', base.task_mgr.stop)
base.set_frame_rate_meter(True)

game_of_life = GameOfLife(resolution=256, pattern=Pattern.RANDOM)
cm = CardMaker('card')
card = render.attach_new_node(cm.generate())
game_of_life.shade(card, swap_tex_at=0)

base.run()
