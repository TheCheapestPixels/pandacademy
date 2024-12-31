# In `main_basic_compute.py` I started out by motivating the use of
# compute shaders by talking about the raw computing power that it
# brings to the table. Here we will apply that power to Conway's Game of
# Life, probably the most well-known cellular automaton.
#
# So, what is *that*? Take a grid paper; Each box is a cell that can be
# either alive or dead. If it is alive and has two or three living
# neighbors, it will remain alive, otherwise it dies; If it is dead, it
# will become alive again when it has exactly three living neighbors.
# Apply this rule to each cell of the grid at the same time, first
# determining the future state of each cell, then updating the state,
# and that's it.
#
# Theoretically, all of this happens on an infinitely large plane, but
# because memory is finite, we will use a texture, and make its borders
# wrap around, as if the horizontal edges are glued to each other, and
# the same for the vertical ones. This also eliminates some edge cases
# (ha ha) in handling the edges.


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


# For debugging and experimentation purposes, we will set up a few
# classical patterns with which to start the game instance.
class Pattern(Enum):
    BLANK = 0
    RANDOM = 1
    SPINNER = 2
    GLIDER = 3
    PENTOMINO = 4


shader_source = """#version 430

layout (local_size_x = 16, local_size_y = 16) in;

// We will again use an input and an output texture, for reasons that I
// will explain below.
layout(rgba32f) uniform image2D fromTex;
layout(rgba32f) uniform writeonly image2D toTex;

// Some helpful constants to make the code more readable.
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

void main() {
  ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
  // First, is this cell alive?
  bool amAlive = imageLoad(fromTex, coord).r == 1.0;
  // ...and how many neighbors are?
  vec4 neighs = imageLoad(fromTex, donutCoord(coord + bottomLeft)) +
                imageLoad(fromTex, donutCoord(coord + bottomMiddle)) +
                imageLoad(fromTex, donutCoord(coord + bottomRight)) +
                imageLoad(fromTex, donutCoord(coord + middleLeft)) +
                imageLoad(fromTex, donutCoord(coord + middleRight)) +
                imageLoad(fromTex, donutCoord(coord + topLeft)) +
                imageLoad(fromTex, donutCoord(coord + topMiddle)) +
                imageLoad(fromTex, donutCoord(coord + topRight));
  int livNeighs = int(neighs.r);

  // So, will the cell live? Does it have three living neighbors, or is
  // it alive and has two living neighbors?
  bool willBeAlive = (amAlive && livNeighs==2) || (livNeighs==3);

  // Now that we know, let's get the information into the texture.  
  imageStore(toTex, coord, vec4(willBeAlive, 0., 0., 1.));

  // One might think that instead of storing into a second texture, we
  // could invoke a memory barrier, making all compute shader instances
  // wait until all others have reached the barrier as well, and only 
  // then store the data back into the input texture. That would look
  // about like this:
  //
  //   memoryBarrierImage();
  //   imageStore(fromTex, coord, newCell);
  //
  // Well, nope! Memory barriers only work within a workgroup, and each
  // workgroup works on a 16x16 tile, so we do not know when the
  // bordering tiles will be updated, and their computations will also
  // depend on the input of *this* workgroup's tile. So, no, this
  // doesn't work, but we should keep it in mind for the next 
  // improvement.
}
"""

# The rest of the code is merely the infrastructure to get something on
# the screen, with some bells and whistles added for debugging purposes
# and for the sheer fun of it. Hence only the code relevant to this
# lesson will be commented.


# Objects of this class will manage a nodepath each, setting up its
# copute node and updating its texture attribute.
class GameOfLife:
    def __init__(self, resolution=64, pattern=Pattern.RANDOM):
        self.resolution = resolution
        # Because we will pingpong the textures before the first
        # invocation of the shader, we paint the input on the "output"
        # texture.
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
        # Remember the dummy node from the basic example? This time we
        # do actually want this node in the scene, so that the shader is
        # invoked automatically during rendering...
        node = ComputeNode("compute")
        node.add_dispatch(16, 16, 1)
        compute_np = NodePath(node)
        compute_np.set_shader(self.shader)
        compute_np.set_shader_input("fromTex", self.texture_in)
        compute_np.set_shader_input("toTex", self.texture_out)
        self.compute_np = compute_np

    def shade(self, nodepath, swap_tex_at=0):
        # ...and so we do attach it, and add the pingpong task...
        self.nodepath = nodepath
        nodepath.set_texture(self.texture_in)
        self.compute_np.reparent_to(nodepath)
        base.task_mgr.add(self.swap_textures, sort=swap_tex_at)

    def swap_textures(self, task):
        # ...which does some variable juggling...
        old_tex_in = self.texture_in
        old_tex_out = self.texture_out
        self.texture_in = old_tex_out
        self.texture_out = old_tex_in
        # ...and updates the textures on shader and node.
        self.compute_np.set_shader_input("fromTex", self.texture_in)
        self.compute_np.set_shader_input("toTex", self.texture_out)
        self.nodepath.set_texture(self.texture_in)
        return task.cont


ShowBase()
base.cam.set_pos(0.5, -2.0, 0.5)
base.accept('escape', base.task_mgr.stop)
base.set_frame_rate_meter(True)

# This is where you fiddle with parameters for fun.
game_of_life = GameOfLife(resolution=256, pattern=Pattern.RANDOM)
cm = CardMaker('card')
card = render.attach_new_node(cm.generate())
game_of_life.shade(card, swap_tex_at=0)

base.run()
