GPU Rendering
-------------

Graphics cards, a.k.a. GPUs (Graphics Processing Units) are a kind of
computer inside your computer; They (usually) have their own memory,
their own processors, and an architecture that is fascinatingly
different from that of your actual computer. GPUs aren't fully
autonomous computers, though, but instead get controlled by commands and
data issued by programs running on the CPU.


Compute Shaders
===============

GPUs have specialized processors for operations relevant to rendering,
and their architecture is optimized for that purpose. While that was of
course their original purpose, clever people have begun abusing that
rendering process to do more general-purpose kinds of computation.
Eventually, OpenGL extensions and dedicated APIs were created to
streamline the process, resulting in today's compute shaders.

Why go over these first, though, especially when the point of this
course is to explain the rendering process? Because...
* they are not fundamentally different from visual shaders; They too are
  programs transforming input data into output data.
* they are basically the simplest kind of shader there is, and do not
  require much explanation to get started with.
* having basic knowledge of compute shaders will make reading up on
  graphical shaders much simpler.
* compute shaders are ubiquitous these days for processing data that
  will eventually wind up in the rendering process or even game
  mechanics.
* apparently they are *so* popular that some engines have stopped using
  the rasterizer pipeline at all, opting to do even these tasks in
  compute shaders.

The [first example](shaders/compute/main_basic_compute.py) that we will
go over shows how we
* manage the flow of texture data from CPU to GPU and back,
* dispatch a compute shader to process texture data on the GPU.

Next, we introduce
[Shader Storage Buffer Objects](shaders/compute/main_ssbo.py) as another
way to organize your data, making it easier to work with.

At this point, you're already prepared to dive into graphical shaders,
but if you stick around, then next, we will implement
[Conway's Game of Life](shaders/compute/main_game_of_life.py) and deal
with problems that arise from how compute shaders work. Long story
short, this is how to screw up:
* Write back into the input texture. Race condition between workgroups
  result.
* Load the Moore neighborhood of each texel; Memory bus performance
  evaporates. Instead, preload the data into shared memory.

What you should ignore right now are my
[first](shaders/compute/main_game_of_life_2.py) and
[second](shaders/compute/main_game_of_life_3.py) attempt to improve
the Game of Life's performance; Profiling does so far show an actual
*decrease* in performance.


Graphical Shaders
-----------------

* [Minimal shader example](shaders/minimal/shader.py) demonstrates
  vertex and fragment shader. That is sufficient to explain the default
  shading pipeline, and show off first tricks.
* [All-stages example](shaders/all_stages/shader.py)
  * all five rendering shaders in action
  * hardware instancing.
* [Pandatoy](pandatoy/main.py) is a small tool akin to the website
  [Shadertoy](https://www.shadertoy.com/), albeit with a much reduced
  feature set.
* [HotShader](pandatoy/hotshader.py) is a cut-down version of Pandatoy
  that you can plug into your own programs to shade arbitrary objects,
  and have the same hotload functionality.


Notes
-----

* Pipeline
  1. Vertex shader
  2. Tessellation Control / Evaluation shaders, Geometry shader
  3. Rasterization
  4. Fragment shader
  5. Depth Test
* Early Fragment Test (a.k.a. Early Depth Test or Early Z-Test):
  Usually, depth testing happens after the fragment shader. If no
  fragment shader is present, or it neither uses the `discard` keyword
  nor writes to `gl_FragDepth`, then the test can be done before
  fragment shading, and if the fragment gets rejected, the fragment
  shader won't be executed.
