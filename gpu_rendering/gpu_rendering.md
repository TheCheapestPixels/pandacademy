GPU Rendering
=============

Graphics cards, a.k.a. GPUs (Graphics Processing Units) are a kind of
computer inside your computer; They (usually) have their own memory,
their own processors, and an architecture that is fascinatingly
different from that of your actual computer. GPUs aren't fully
autonomous computers, though, but instead get controlled by commands and
data issued by programs running on the CPU.


Compute Shaders
---------------

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

What *is* the difference between compute and other shaders? They are
invoked to fulfill some function within the rendering process, and for
that purpose, they get access to specific inputs, outputs, and
operations. So let's go over how that rendering process works.


### Vertex Data

As you saw in the chapter about geometric modeling, models are made from
triangular faces, which are connecting the model's vertices. These
vertices are specified in the model's space (or, more verbosely, in the
coordinate system that is relative to the model's origin).

For completeness' sake it should be mentioned that triangles are not the
only primitive available. There are:
* The basic primitives; Points, lines, triangles, quads, and polygons.
* Strips, which are sequences of lines, triangles, or quads, and thus
  save on memory use; If you have a strip of 100 lines, you need to
  store the starting point for the first line, but every line after that
  uses the end point of the line before it as their starting point.
* Triangle fans, which work like triangle strips, except that the
  triangles are around a common point.
* Patches, which are sets of vertices, which will be turned into
  geometry by geometry or tessellation staders.

Scenes as a whole contains models, cameras, and lights. While that was
not an exhaustive list, it suffices to get basic graphics going. At the
point that we are at now, a camera (from which's perspective we want to
render something) has been selected, as well as the model that we want
to render *right now*. Other models may have been rendered already.


### The Pipeline

The actual process is, depending on how closely you want to look at it,
actually really simple, manageably complex, or absurdly intricate.

The simplest version is the one that will dominate the rest of the
course:
* Vertex Shader: We do math on every vertex to get its on-screen
  position and depth.
* Rasterizer: The GPU turns our primitives into fragments, which are
  basically pixels-to-be, consisting of a bunch of data that describes
  the point on the primitive that corresponds to a pixel.
* Fragment Shader: We process each fragment, calculating its output
  values. Typically this is a color, and possibly an update to its depth
  value.
* Depth Test: If the fragment is behind an already known fragment at the
  same pixel position, it is discarded; If it is in front of it, it
  replaces it.

While assembling the final output image's colors, the GPU
  also keeps track of how far away each pixel generated so far is.
  * If there is no recorded fragment at this position yet, we have one
    now.
  * If the new fragment is behind an opaque one (at the same pixel
    position), it is not visible, and gets discarded.
  * If it is in front of a recorded pixel, two things may happen:
    * If the new fragment is opaque, it simply replaces the current
      pixel.
    * If it is transparent, it gets blendes it with the existing one,
      and the depth value is *not* updated.

At the intermediate level, there are several additional forms of shaders
available. On one hand, the pipeline as described above has been added
to:
* Vertex Shader
* Tessellation Shader: This shader consists of two components, which
  together turn a patch primitive into a continuous surface of
  primitives.
  * Tessellation Control Shader: Here we define how finely broken down
    we want the surface to be.
  * Tessellator: Generates the primitives.
  * Tessellation Evaluation Shader: Now we can basically vertex shade
    the vertices of the generated primitives.
* The Geometry Shader: We can process each primitive again, possibly
  creating even more, or discarding them,
* Rasterizer
* Fragment shader
* Depth Test

For curiosity's sake, here is [an example](shaders/all_stages/shader.py)
that makes use of all the shaders in the classic pipeline, plus hardware
instancing.

However, since this pipeline has proven unsatisfying in practice, as it
introduces an overhead and bottlenecks due to switching between
processing vertices and primitives, a wholly new approach has been
introduced to replace the part of the pipeline before the rasterizer:
* Task Shader: Processes how many meshes to create.
* Mesh Generation: Create the meshes.
* Mesh Shader: Generate primitives. Like Compute Shaders, these can pull
  in any kind of data.
* Rasterizer
* Fragment Shader
* Depth Test

If you want the highest performance, you have to know how the GPU does
what it does, which goes beyond how the API to work with it works. This
is about the actual algorithms that are etched into its silicon (or at
least into the microcode). This level of detail goes beyond the scope of
this course (and frankly, at this moment, it goes over my head as well.
It can be found though in
[this series of blog posts](https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/).

Again, the rest of this course will use only Vertex and Fragment
shaders. Tessellation and Geometry shaders still occasionally find use,
while Task and Mesh shaders shape up to be the Next Big Thing. Both go
beyond the level that this course aims to provide.


### Vertex shading

The first thing that has to happen is that we find out where each vertex
should end up on the screen. The most typical case is this:

* Local Space: The coordinates are given in the model's space.
* Model Matrix: The model has a position in world space (the scene graph
  root's local space). The transformation between local and world space
  is given by the Model Matrix.
* World Space: `vertexInWorldSpace = ModelMatrix * vertexInLocalSpace;`
* View Matrix: We actually need the vertex position relative to the
  camera, which is called the View Space. The transformation from world
  to view space is given by the View Matrix.
* View Space: `vertexInViewSpace = ViewMatrix * vertexInWorldSpace;`
* Projection Matrix: Now the vertex in view space isnt good enough
  anymore; Now we want it in the space defined by the camera's frustum.
  if the vertex is at the far left edge, we want it at an `x = -1`, no
  matter how far from the camera it is. In fact, we want all coordinates
  to be in a unit cube (from -1 to 1). Barely surprising, that
  transformation is given by the projection matrix.
* Clip Space: `vertexInClipSpace = ProjectionMatrix * vertexInViewSpace;`

Clip space coordinates are what gets fed into the rasterizer.


### Rasterization

While vertex shading allows for programmability, with the above
explanation being the typical program, rasterization is a configurable,
but not a programmable process.

In its basic form, rasterization i a very straightforward process. Clip
space says where on the screen the geometry will end up, we just need to
compress it from 3D space into a 2D plane and transform that to screen
coordinates; This is the Viewport Transformation into Screen Space. In
between, however, we also need to turn our continuous space into
discrete pixels. To do this, the rasterizer basically puts a sheet of
graph paper over the viewer's end of the clip space, and for each
triangle and each cell of the grid it asks "Is the center of the cell on
this triangle?" If not, the triangle doesn't affect this pixel; If it
is, then it does, and a fragment is created.

Besides the coordinate in Clip Space and Screen Space, the fragment also
gets the data from the columns of the vertices that corner the
primitive. The data that the vertices carry gets interpolated, based on
the distance of the fragment from each of the vertices. So if, for
example, the vertices have texcoords, then the fragment will get the
interpolated texcoord for its position on the triangle.


### Fragment shading

Now we are at the stage where we have all the data to calculate what
color should appear on the screen, or, more generally, with what data we
want to represent it. So that is what we do. We have the interpolated
vertex data at hand, any textures and other data that may have been
provided, so we do the math and write the result into the appropriate
output.


### Depth Test

While processing the fragments and assembling their color outputs into
the final image, the pipeline also keeps track at what depth those
fragments were at, creating a corresponding image that, in the end,
shows the depth of the rendered image.

The depth of a new fragment gets compared to the recorded depth at the
coordinate.
* If there is no record, the fragment is accepted, and its depth
  recorded.
* If the fragment is in front of the recorded depth, it replaces the
  already recorded one, and updates the depth.
* If it is behind the recorded depth, it gets discarded.

However, this is only the basic functionality. It can be configured so
that...
* the depth test passes when the fragment's depth is greater, less,
  equal, equal or less, equal or more, or unequal to the recorded depth.
  Or that it passes always, or never.
* the depth of a fragment is not recorded, even if it passes the test.

In Panda3D, these settings are on a per-NodePath base. For details,
[this is the manual page](https://docs.panda3d.org/1.10/python/programming/render-attributes/depth-test-and-depth-write).


Code
----

FIXME: This would be better if it was interspersed with the course.

* [Minimal shader example](shaders/minimal/shader.py) demonstrates
  vertex and fragment shader.
* [Pandatoy](pandatoy/main.py) is a small tool akin to the website
  [Shadertoy](https://www.shadertoy.com/), albeit with a much reduced
  feature set.
* [HotShader](pandatoy/hotshader.py) is a cut-down version of Pandatoy
  that you can plug into your own programs to shade arbitrary objects,
  and have the same hotload functionality.
