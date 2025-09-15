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

First, two small tools to help you in the process of tinkering with
graphical shaders:
* [Pandatoy](pandatoy/main.py) is a small tool akin to the website
  [Shadertoy](https://www.shadertoy.com/), albeit with a much reduced
  feature set.
* [HotShader](pandatoy/hotshader.py) is a cut-down version of Pandatoy
  that you can plug into your own programs to shade arbitrary objects,
  and have the same hotload functionality.

What *is* the difference between compute and other shaders? They are
invoked to fulfill some function within the rendering process, and for
that purpose, they get access to specific inputs, outputs, and
operations. So let's go over how that rendering process works.


### Vertex Data

As you saw in the chapter about geometric modeling, models are made from
triangular faces, which are connecting the model's vertices. These
vertices are specified in the model's space (or, more verbosely, in the
coordinate system that is relative to the model's origin).

Scenes as a whole contains models, cameras, and lights. While that was
not an exhaustive list, it suffices to get basic graphics going. At the
point that we are at now, a camera (from which's perspective we want to
render something) has been selected, as well as the model that we want
to render *right now*. Other models may have been rendered already.


### The Pipeline

The actual process is, depending on how you want to look at it, actually
really simple, manageably complex, or absurdly intricate.

If you want the highest performance, you have to know how the GPU does
what it does, which goes beyond how the API to work with it works. This
is about the actual algorithms that are etched into its silicon (or at
least into the microcode). This level of detail goes beyond the scope of
this course (and frankly, at this moment, it goes over my head as well.
It can be found though in
[this series of blog posts](https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/).

At the intermediate level, we have two pathways that lead to the
rasterizer. The "classic" route is that...
* Vertex Data gets fed into the...
* Vertex Shader, which outputs updated vertex data, which the...
* Tessellation stage breaks down into even more triangles by letting
  the...
  * Tessellation Control Shader select the settings by which the...
  * Tessellator generates the triangles, which the...
  * Tessellation Evaluation Shader then equips with data.
* The Geometry Shader then does processes the triangles, possibly
  creating even more, or discarding them, until we finally reach the
* Rasterizer, which turns the triangles into fragments.

A newer approach is that a...
* Task Shader generates work for the...
* Mesh Generation, which outputs data that is fed into the...
* Mesh Shader, which generates the geometry data that gets fed into
  the...
* Rasterizer.

In either approach, the...
* Rasterizer generates fragments which are then processed by the...
* Fragment Shader, which outputs the final data, e.g. a pixel's color,
  which gets inserted or blended into the final image, or gets
  discarded, based on the...
* Depth Test.

This is a sensible level of detail to get started with, and it hits all
the big steps of the process. However, the new approach requires very
modern hardware, and the older one has several stages that do not get
much use, specifically Tessellation and Geometry Shading. Thus, we will
start at an even more simplified the model, which covers a wide swath of
use cases. For curiosity's sake, here is
[an example](shaders/all_stages/shader.py) that makes use of all the
shaders in the classic pipeline, plus hardware instancing.

The simple model is:
* Vertex Data: We have already dealt with how to create this in the
  course on
  [Geometric Modeling](../geometric_modeling/geometric_modeling.md).
* Vertex Shader
* Rasterizer
* Fragment Shader
* Depth Test


### Vertex shading

The first thing that has to happen is that we find out where each vertex
should end up on the screen. The simplest case is this:

* The coordinates are given in the model's space, a.k.a. local space.
* The model has a position in world space (the scene graph root's local
  space).
* The transformation between local and global space is given by the
  model matrix, meaning that
  `vertexInWorldSpace = ModelMatrix * vertexInLocalSpace;`
* While that is a start, we actually need the vertices relative to the
  camera, which is called the view space. The transformation from world
  to view space is given by the view matrix:
  `vertexInViewSpace = ViewMatrix * vertexInWorldSpace;`
* FIXME: Projection matrix


### Rasterization

FIXME


### Fragment shading

FIXME
* [Minimal shader example](shaders/minimal/shader.py) demonstrates
  vertex and fragment shader.
