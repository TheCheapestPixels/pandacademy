# By now you are maybe sick of working with textures, and/or are
# wondering what else there is; Is there really no better way than
# encoding all the data as images?
# Yes, there is, and it is called Shader Storage Buffer Objects, SSBO
# for short, and "it's just arrays..." for people like me.
#
# Let's do something super-simple: We create a handful of numbers
# between 0.0 and 1.0, store them in an SSBO, let a shader go
# `x = 1.0 - x` on them, transfer them back into CPU land, and convert
# them into Python floats.


from array import array

from panda3d.core import NodePath
from panda3d.core import Shader
from panda3d.core import ShaderAttrib
from panda3d.core import ShaderBuffer
from panda3d.core import GeomEnums

from direct.showbase.ShowBase import ShowBase


ShowBase()
base.cam.set_pos(0.5, -2.0, 0.5)
base.accept('escape', base.task_mgr.stop)


num_elements = 2**5
initial_data_py = [i / (num_elements - 1) for i in range(num_elements)]
# On the Panda3D side, we call an SSBO a ShaderBuffer, and to store data
# in it, we first need to convert it into bytes.
initial_data_bytes = array('f', initial_data_py).tobytes()
# If you do *not* want to provide initial data, probably because you are
# generating it on the GPU itself, just pass how many bytes you want to
# be allocated. Here it would be `num_elements * 4`, as each float has
# four bytes.
# The usage hint determines where the data will reside. `UH_client` will
# put the data into the host machine's memory, while all other options
# put it into VRAM. Historically, there was a difference between
# `UH_stream`, `UH_dynamic`, and `UH_static` (from "close to host" to
# "on VRAM and doesn't get updated from the CPU"), but, well, that's
# history now.
# The name, here `DataBuffer`, will be used in the shader to identify
# the buffer.
ssbo = ShaderBuffer(
    'DataBuffer',
    initial_data_bytes,
    GeomEnums.UH_static,
)


shader_source = """#version 430
layout (local_size_x = 32, local_size_y = 1) in;

// This bit of code is utterly superfluous, as it is just another name
// for `float`. But while we are here: When you work on structs with
// multiple fields, and your shader only uses a few of those, then only
// those will be transferred from memory to the compute units.
struct Data {
  float value;
};

// This is the actual SSBO. An SSBO can contain several arrays, and on
// the last one, you don't have to specify a size, because its size can
// be inferred from the size of the buffer.
// `std430` defines the memory format, and is the only currently useful
// option. Older cards improved performance by padding their memory
// representations; That is now detrimental.
layout(std430) buffer DataBuffer {
  Data data[];
};

void main() {
  int idx = int(gl_GlobalInvocationID.x);
  data[idx].value = 1.0 - data[idx].value;
}
"""

# From here on out, you have already seen everything.

# Setting up the shader
shader = Shader.make_compute(Shader.SL_GLSL, shader_source)
np = NodePath("dummy")
np.set_shader(shader)
np.set_shader_input("DataBuffer", ssbo)


# The dispatch
workgroups = (num_elements // 32, 1, 1)
sattr = np.get_attrib(ShaderAttrib)
base.graphicsEngine.dispatch_compute(
    workgroups,
    sattr,
    base.win.get_gsg(),
)


# Extract data
engine = base.win.gsg.get_engine()
data_bytes = engine.extract_shader_buffer_data(ssbo, base.win.gsg)
data_py = array('f', data_bytes).tolist()


# Show the results
for old_data, new_data in zip(initial_data_py, data_py):
    print(f"{old_data:1.3f} -> {new_data:1.3f}")
