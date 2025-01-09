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
from panda3d.core import SamplerState

from direct.showbase.ShowBase import ShowBase


class Pattern(Enum):
    BLANK = 0
    RANDOM = 1
    SPINNER = 2
    GLIDER = 3
    R_PENTOMINO = 4


def make_initial_image(resolution, pattern):
    image = PfmFile()
    image.clear(
        x_size=resolution,
        y_size=resolution,
        num_channels=4,
    )
    image.fill(Vec4(0, 0, 0, 1))
    offset = resolution // 2
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
    elif pattern == Pattern.R_PENTOMINO:
        image.set_point(offset - 1, offset    , 1)
        image.set_point(offset - 1, offset + 1, 1)
        image.set_point(offset    , offset - 1, 1)
        image.set_point(offset    , offset    , 1)
        image.set_point(offset + 1, offset    , 1)
    else:  # Pattern.RANDOM
        for x in range(resolution):
            for y in range(resolution):
                image.set_point(x, y, random.randint(0, 1))
    return image


shader_source = """#version 430

layout (local_size_x = 16, local_size_y = 16) in;

layout(rgba32f) uniform image2D fromTex;
layout(rgba32f) uniform writeonly image2D toTex;

shared float tile[18][18];

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

// The idea behind this approach is that we have got 256 invocations to
// load 324 texels; If every invocation loads two, 68 texels will be
// loaded twice, but that's the memory bandwidth tax we're willing to
// pay so that the loading can be branchless and still simple. If you
// know of an even better approach, please file a GitHub issue.

// So, first we need to know the how manyeth invocation in a workgroup
// we are working on.
int invocationIndex() {
  int index = int(gl_LocalInvocationID.y * 16 + gl_LocalInvocationID.x);
  return index;
}

// We also need a way to turn indices back to 2D coordinates on the
// shared tile.
ivec2 indexToTileCoord(int index) {
  // Since the index may be out of bounds, first let's get it back into
  // bounds again.
  index = index % 324;  // 18*18
  // Turning that into x and y portions is trivial.
  ivec2 tileCoord = ivec2(floor(index / 18), index % 18);
  return tileCoord;
}

// Now, given the index of the piece of the tile that we want to load...
void loadToTile(image2D tex, int index) {
  // ...we need the coordinate on the tile...
  ivec2 tileCoord = indexToTileCoord(index);
  // ...and the corresponding coordinate on the image.
  ivec2 imgCoord = ivec2(gl_WorkGroupID.xy) * 16 + tileCoord + bottomLeft;
  imgCoord = donutCoord(imgCoord);
  // Looks like we have everything that we need. So let's go!
  tile[tileCoord.x][tileCoord.y] = imageLoad(tex, imgCoord).r;
}

// With everything in place to load one texel, we now can load all the
// texels in one fell swoop.
void preloadTile(image2D tex) {
  // We load two texels per tile, so the index of the first of those is
  // twice that of the invocation that does the loading, and the second
  // is, to nobody's surprise, one more.
  int baseIndex = invocationIndex() * 2;
  // Since all the hard work is done already...
  loadToTile(tex, baseIndex);
  loadToTile(tex, baseIndex + 1);
  // And now we need to synchronize the invocations in ths workgroup.
  barrier();
}

float fetchTile(ivec2 coord) {
  return tile[coord.x][coord.y];
}

void main() {
  preloadTile(fromTex);
  ivec2 coord = ivec2(gl_LocalInvocationID.xy) + ivec2(1, 1);
  bool amAlive = fetchTile(coord) == 1.0;
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
        image_in = make_initial_image(self.resolution, pattern)
        self.texture_in = Texture('')
        self.texture_in.load(image_in)
        self.texture_in.set_format(Texture.F_rgba32)
        self.texture_in.set_magfilter(SamplerState.FT_nearest)

        self.texture_out = Texture('')
        self.texture_out.setup_2d_texture(
            resolution,
            resolution,
            Texture.T_float,
            Texture.F_rgba32,
        )
        self.texture_out.set_magfilter(SamplerState.FT_nearest)
        self.setup_shader()

    def setup_shader(self):
        for idx, line in enumerate(shader_source.split('\n')):
            print(f"{idx+1:03} {line}")
        self.shader = Shader.make_compute(
            Shader.SL_GLSL,
            shader_source,
        )
        node = ComputeNode("compute")
        node.add_dispatch(
            self.resolution // 16,
            self.resolution // 16,
            1,
        )
        compute_np = NodePath(node)
        compute_np.set_shader(self.shader)
        self.compute_np = compute_np

    def shade(self, nodepath, swap_tex_at=55):
        self.nodepath = nodepath
        self.compute_np.reparent_to(nodepath)
        self.connect_textures()
        base.task_mgr.add(self.swap_textures, sort=swap_tex_at)

    def swap_textures(self, task):
        old_tex_in = self.texture_in
        old_tex_out = self.texture_out
        self.texture_in = old_tex_out
        self.texture_out = old_tex_in
        self.connect_textures()
        return task.cont

    def connect_textures(self):
        self.compute_np.set_shader_input("fromTex", self.texture_in)
        self.compute_np.set_shader_input("toTex", self.texture_out)
        self.nodepath.set_texture(self.texture_in)


ShowBase()
base.cam.set_pos(0.5, -2.0, 0.5)
base.accept('escape', base.task_mgr.stop)
base.set_frame_rate_meter(True)

game_of_life = GameOfLife(resolution=128, pattern=Pattern.RANDOM)
cm = CardMaker('card')
card = render.attach_new_node(cm.generate())
game_of_life.shade(card)

base.run()
