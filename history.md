Computer Graphics
-----------------

* Past
  1. We do everything on the CPU. Professionals have access to Silicon
     Graphics workstations, which include early GPUs.
  2. GPUs are released on the consumer market.
  3. The GPU instruction set becomes enriched with configuration
     options to influence the rendering behavior.
  4. Parts of the pipeline become programmable.
* Present
  * Open Standards: OpenGL, Vulkan, [SPIR](https://www.khronos.org/api/spir)
  * Other standards: Direct3D, Metal
  * Compute and Vertex + Fragment shaders, per-fragment lighting
  * 
* Future
  * Raytracing units proliferate
  * Change in shader architecture
    * Task and Mesh shaders at the beginning of the pipeline
    * Geometry and Tessellation shaders may get dropped
  * Shading languages develop further
    * Shading languages in general become obsolete, as general purpose
      programming languages compile to LLVM, which then gets compiled to
      SPIR-V; Example: [New Circle](https://www.circle-lang.org/)
    * Domain-specific languages may still persist. [Example](https://www.taichi-lang.org/)
  * OpenGL becomes obsolete as Khronos focuses on Vulkan exclusively.
    Kind of example: GL_NV_mesh_shader / VK_EXT_mesh_shader


Panda3D
-------

* Past
  1. Disney Imagineering develops a 3D engine in-house to power VR
     attractions in their theme park, and create tools to prototype
     future rides virtually.
  2. a) Disney open-sources Panda3D, b) CMU uses it as a teaching tool.
* Present
  * Pre-production Vulkan backend
  * SPIR-V support
* Future (hopefully)
  * Panda3D development keeps up with developments in open standards
  * Version 2.0 cuts out a lot of legacy
