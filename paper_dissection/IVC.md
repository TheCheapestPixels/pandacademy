IVC2Panda3D
===========

Foreword
--------

"Interactive Visual Computing" (IVC) is a course at the university of
Hamburg, created as a merger of "Computergrafik und Bildsynthese" (CGB)
and "Realtime Interactive Media" (RTIM).

Video recordings of the course are available at the university's
[Lecture2Go platform](https://lecture2go.uni-hamburg.de/en/l2go/-/get/v/14163). In German.

This document contains
* Takeaways: These are parts of my study notes, and provided again here
  for context. They represent only a fragment of the lecture's content,
  and do not serve as a replacement for partaking in the course.
* Notes on Panda3D: Per-session notes on how to further explore the
  session's content, and also explore Panda3D at the same time.
* Personal notes: Catch-all category for what I have to add.

The intend is two-fold:
* To help me refresh and deepen my knowledge of the basics of computer
  graphics, so as to enable me to do a real deep dive into shaders and
  the innards of Panda3D's renderer.
* To create a supplement for the course for people who want to learn
  about Panda3D while taking the IVC course. As I am already codifying
  my knowledge [here](https://github.com/TheCheapestPixels/pandacademy/tree/IVC),
  I will link to that resource as heavily as possible. In fact,
  everything practical in this file will eventually end up in the
  Pandacademy course, leaving only a few notes and a lot of links, thus
  providing an alternative partial path through the Pandacademy.

Just to be very, VERY clear: Panda3D does and will **not** serve as a
replacement for POVRay, neither in general nor in the context of IVC.
POVRay is a raytracer, Panda3D uses your GPU's rasterizer pipeline.
Panda3D does not come with its own raytracer shader (although such a
project would be much appreciated, especially if also applied to
sound, but then it would still have to go into its own package).

It will **especially not** serve as a medium to achieve your practical
credit for IVC. Neither Panda3D applications nor the content created
by them are admissable in fulfillment of the credit requirements. I,
the author of this document, am in no way affiliated with the
university of Hamburg besides having been a student there once.

That being said: Panda3D
* is very lightweight. It provides a thin wrapping layer over the
  hardware. This gives you
  * tight control your program's behavior; You do not work with high-
    level abstractions, but surprisingly close to the metal.
  * access to data as data; Seeing the actual values of things without
    having to render them as an image... What a concept!
  * very low iteration time; Less than a second between starting your
    program and seeing the result is hardly a brake on your progress.
* provides a Python API.
  * If you don't know Python yet, you will by tomorrow. It is that easy
    to learn. Just dive right into [the documentation](https://docs.python.org/3/index.html).
  * Again, low iteration time. You start the interpreter and your
    program is running.
  * Python has a massive ecosystem of packaged applications and
    libraries.
  * It has been widely adopted in science and industry.

This document is currently in **beta** status: Everything relevant has at least been mentioned, but barely anything up to the intended depth of the topic, with many things indeed only being name-checked.

- [X] Session 1
- [ ] Session 2: This should be preceded by a scene graph tutorial, but
      the relevant lecture for that is lecture 3. It should also be
      preceded by an overview of rasterizer rendering, because right now
      the words "shader inputs" and "`uniform`" are gibberish.
- [ ] Session 3a: Well, here would go the scene graph tutorial...
- [X] Session 3b
- [ ] Session 4: Needs "only" code.
- [X] Session 5
- [ ] Session 6: Camera code examples.
- [ ] Session 7: Ponder intervals



Session 1
---------

### Takeaway

The field of Graphical Data Processing deals with three types of scene
description:
* Semantic: E.g.
 * Natural language "Charlie feeds Snoopy"
 * Knowledge representation formats:
   ```
   (action 'feeds
       (actor 'charlie)
       (target 'snoopy)
   )
   ```
* Geometric: Geometric primitives, their parameters, and spatial
  arrangement.
* Iconic: E.g.
  * `charlie_feeds_snoopy.png`
  * An image on the screen.
  * framebuffer content

Transforming one representation into another is the task of these four
subfields:
* Iconic to geometric: Image Processing / Pattern Recognition
* Geometric to semantic: Image Understanding
* Semantic to geometric: Visualization
* Geometric to iconic: Graphical Data Processing (FIXME: again? We seem
  to be shadowing the name here. This is what IVC is about.

Graphical Data Processing deals with these categories of digital models:
* Images
* Geometry
* Radiometry: Interaction of matter and energy
* Colors
* Digitalization: Turning analog functions into digital data


### Panda3D

Panda3D provides tools to create / load / save / manipulate geometric
scene descriptions, and turn them into iconic representations. It also
does a whole bunch more that is not relevant right now for this course.

As for the models supported:
* Images and videos: In-memory representation is provided through
  * `panda3d.core.PfmFile` for floating valued data
  * `panda3d.core.PNMImage` for integer valued data
  * `panda3d.core.Texture` for uploads to / downloads from the GPU.
  `PfmFile` and `PNMImage` have tools to manipulate individual pixels,
  `Texture` does not.
  
  Lots of file formats are supported for loading *and* saving. (FIXME:
  What libs?) 
* Geometry: In-memory representation happens through lots of classes
  from Panda3D core. For use, one or more of them are put into a node,
  which is a subclass of `PandaNode`. Hierarchy is created as a tree
  (actually a DAG) of `NodePath`s, which may contain `PandaNode`s.

  Loading support is provided through assimp and the `panda3d-gltf`
  package; The latter is what `blender2bam`.

  Panda3D also supports its own file formats `.egg` and `.bam`.
  * `.egg`: A plain-text file format with a restricted syntax, intended
    for backwards compatibility, and will not be changed.
  * `.bam`: The binary format that features have been added to over
    time.
* Radiometry: This topic we will deal with in shaders, which can be
  written in GLSL or HLSL, or be provided in SPIR-V.
* Colors: I know of nothing besides RGB and sRGB. There are Python
  packages like `Colour` and `colorio` though.
* Digitalization: Yeah, no, you're on your own.

Homework: Install Panda3D and make sure that it is running.
[Here is the tutorial.](../hello_panda3d/hello_panda3d.md)


### Personal notes

I recommend the use of
* `.png` for images; It's lossless, and disk space is cheap now.
* `.gltf` / `.glb` for importing models; It's the Khronos standard
  called glTF, because shadowing words is fun. `.gltf` uses JSON to
  encode model information in a somewhat human-readable way, while
  `.glb` is the binary format, and thus loads faster.

  Sadly it is currently not supported as an output format to write files
  with, that would be helpful for e.g. tools to procedurally generate
  models with.
* `.bam` for scene graphs: It's as easy as
  `my_nodepath.write_bam_file(filename)`. Do note that Python tags on
  the NodePaths would not be serialized.
* GLSL for shaders; Again, because it's the Khronos standard.

Also I think that the diagram of scene descriptions lacks horizontal
arrows for transformations within the types of scene descriptions.


Session 2
---------

## Takeaway

There are classes of coordinate systems (e.g. cartesian, polar). Within
each class there are types that define e.g. the relative arrangement of
axes, directions of rotation, how vectors and matrices represent either,
and how many dimensions are used.

Instances of coordinate systems can be put into relation with one
another mathematically, creating hierarchies.

There are four basic types of transformation within a single coordinate
system; From these, all other transformation can be created:
* Translation
* Rotation
* Scaling
* Shearing

Each can be represented as an affine transformation of homogeneous
coordinates.
* Homogeneous coordinates: For n-dimensional coordinates, we use an
  n+1-dimensional vector, and the last element is 1.
* Affine transformation: Like a linear transformation, but the last
  column of the matrix (or row, depending on the mathemagician's
  choice) is the same as in the identity matrix.

E.g. in 2D:
```
new_ pos = transform * old_pos

          (a b 0)             (x*a + y*c + e)
new_pos = (c d 0) * (x y 1) = (x*b + y*d + f)
          (e f 1)             ( 0  +  0  + 1)
```
Thus,
1) An affine transformation times a homogeneous coordinate is again a
   homogeneous coordinate (the third vector element is always 1).
2) The values `e` and `f` are added as-is to the rotated/scaled/sheared
   x/y values, thus the translation is added "after" the rotation.

Multiplying the matrices means concatenating the operations that they
represent, and multiplying a vector with the matrix means transforming
it through all those operations.

POVRay has a `clock` variable.


### Panda3D

Well, now we're cooking with gas!
```python
from math import pi
from panda3d.core import NodePath


# First, let's create a scene graph.
root = NodePath("Root of the scene graph")
child = root.attach_new_node("Child node")
# What is the transformation matrix between the coordinate systems of
# these NodePaths?
print(child.get_mat())  # This shows the identity matrix.
# So how is the matrix oriented? Let's use a translation to check.
child.set_pos(2, 3, 4)
print(child.get_mat())  # The parameters show up in the bottom row.
```

The coordinate system's style can be configured, but the default is
Palm-Up Righthanded:
* x to the right
* y forward
* z up
* Pitch turns around x
* Roll turns around y
* Yaw is called heading, and turns around z

Vector formats typically are
* position: `xyz` (with w being a perspective factor discussed later),
  but on the GPU, in fragment shaders `xyzw` is used, with `w` being
  the perspective factor.
* rotations: `hpr` order, meaning that they turn around axes `zxy`.
* colors: `rgb` and `rgba` are the most common ones. `a` stands for
  `alpha` and means opacity, where 1.0 stands for "fully opaque", and
  0.0 for "fully transparent".
* normals: Normalized `xyz` vectors in object space, but scaled to
  `[0.0, 1.0]` when used in textures, where it also is in UV space.

Each `NodePath` contains the transformation between the `PandaNode` of
its parent and its own.

The Model / View / Projection matrices and their combinations are
available as
[shader inputs](https://docs.panda3d.org/1.10/python/programming/shaders/list-of-glsl-inputs#uniform-shader-inputs):
```glsl
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ViewProjectionMatrix;
```

The use of scaling is discouraged, as there may still be bugs relating
to it be hiding in the collision system, and the Bullet wrapper does not
support it at all. Shearing is not supported by the API.

Panda3D has a clock, too, and it too is added to `__builtin__` as
`globalClock`, but is also available as `base.task_mgr.clock`.

```python
from direct.showbase.ShowBase import ShowBase


ShowBase()

def print_time(task):
    c = base.task_mgr.clock
    print(c.dt, c.frame_time, c.real_time, task.time)
    return task.cont

base.task_mgr.add(print_time)
base.run()
```

Observe what happens when you hide the Panda3D window.


### Personal Notes

Do not skimp on the math. When being asked "How do you calculate the
angle between two vectors?" in a job interview, "`v_a.angle(v_b)`?" is a
good first answer, but a follow-up of "`acos` of the dot product of the
normalized vectors" will still be expected. 

In practice though, once you have understood it, do skimp on the math
wherever you can. Long equations do not make for readable code, and the
only practical use of making your own life harder is recreation.


Session 3a
----------

### Panda3D

This session showed the power of hierarchies of coordinate systems.
FIXME: The aforementioned missing scene graph tutorial. 


Session 3b
----------

### Takeaway

Geometric Modeling: How do represent an object as data?
* Volume based
  * octree: Recursively splitting a cube into eight cubes
  * CSG: Set operations to combine primitives
* Surface based: Next week


###  Panda3D

GPUs work with surface-based models. See you next week!


# Personal notes

Octrees are not just for saying whether an object is or isn't there.
Each leaf of the tree can contain a reference to arbitrary data. In that
form, they are simple space partitioning algorithm, may speed up many
other algorithms by providing e.g. fast nearest-neighbor lookup. Of
course they *can* also still be used for geometric models, but you can
also store surface properties like normals or materials in them.


Session 4: Projections
----------------------

### Takeaway

Projections are transformations from one coordinate space into another,
here in practice only planar 3D into 2D. Starting with distinguishing
between parallel and central projection, lots of types of projections
are derived.


### Panda3D

FIXME
* camera lens, reprojection, maybe near/far plane (see session 6)
* `.get_relative_*` and net transformation.


Session 5: Geometric modeling
-----------------------------

### Panda3D

GPUs, and by extension Panda3D, model geometry in terms of
* vertices: Points of data stored in tables with named columns of
  scalars or vectors. Examples of typical columns are
  * `vertex`: position in `vec3`
  * `texcoord`: UV coordinates of a texture at this vertex, `vec2`
  * `normal`: Normal vector for this vertex, `vec3` in object space
* primitives:
  * Points
  * Lines
  * Triangles, specifically single-sided ones with counter-clockwise
    winding order.

[This course](../geometric_modeling/geometric_modeling.md) goes through
the process of defining geometry and animation.

`LineSegs` and `CardMaker` (both in `panda3d.core`) should also be
mentioned; The former is a helper to create meshes made of line
primitives, the latter creates rectangular meshes made from two
triangles, which are a valuable tool for experimenting with textures.


### Personal notes

Points and lines may or may not be supported by any given GPU, and if
they are, support may be lackluster (like e.g. line thickness being
ignored). They are apparently treated as an artifact from a bygone era
by GPU manufacturers.

There are also TriangleFans, TriangleStrips, etc.; These are more
compact representations of series of triangles. Using them saves memory
and transfer time, which are basically two of the three restraints that
we work under on the GPU (with the third being code execution time).


Session 6
---------

### Panda3D

Depth of field, chromatic aberration, bokeh, and all the other
inaccuracies and effects of natural (or fictional) cameras will have to
be faked and approximated. Not here, not now.

Higher-than-3-dimensional spaces are not supported by Panda3D; You will
have to come up with a way to represent your scenes and project them
into the scene graph yourself. If you can do so in shaders, I would like
to know how.

Front / back plane are called near / far plane in Panda3D.
FIXME: Example
FIXME: Lens types?


Session 7
---------

### Panda3D

This lecture is of interest for libraries that generate and work with
models and textures, and also for tessellation shaders.

There is nothing about topology in Panda3D.

FIXME: Also `Intervals`? This wasn't the spline lecture, right?

Homework: Put your knowledge about creating geometry to use by writing a
function that turns spline parameters into a `Geom`. Note: You will soon
find that with increasing resolution, the generation time becomes
prohibitive. This is exactly what Python does not natively excel it.
Computations like this are usually relegated to `numpy`, which does the
math in C++. Also this specific task is what tessellation shaders are
great at, though mesh shaders may replace them in a few years.


### Personal notes

More on splines: ["The Continuity of Splines"](https://www.youtube.com/watch?v=jvPPXbo87ds)


Session 8
---------

### Panda3D

Panda3D light sources are pretty much equivalent to the POVRay ones.
However, they will not cast shadows by default. 
FIXME: Types of light sources, https://docs.panda3d.org/1.10/python/programming/render-attributes/lighting

There are no volume light sources (without raytracing).

Refraction effects need to be faked. Keep the math in mind, it will be
helpful when we write fragment shaders, or calculate the color of
blackbody lights.


Session 9
---------

### Panda3D

WARNING! Computer graphics may cause photosensitive epilepsy. Please
read [this article](https://en.wikipedia.org/wiki/Denn%C5%8D_Senshi_Porygon).

That being said, if your screen supports a high enough framerate, you
can replicate the experiment with the rotating disc of spectral colors.
Alternating between two contrasting colors is also an option.
FIXME: Code

For the topology part, there is again no direct applicability.


### Personal notes

While we are on the topic of the dangers of computer science:
* Therac-25, the radiation therapy machine that killed six people
  through a race condition caused by too competent users.
* "IBM and the Holocaust" by Edwin Black


Session 10
----------

* `00:07:06`: Aerosol scattering and emitting / absorbing media
* `00:42:25`: Color models

Atmospheric effects can be achieved through raymarching. Emitting media
I frankly do not know about.

The color model part is massively important.
FIXME: Example of changing the framebuffer's default color to allow for
experiments, encourage use of tasks and events.


Session 11
----------

### Panda3D

I will not address the algorithms in this lecture. Instead I will point
that so far we have only talked about writing model data, and that to
apply algorithms to given models you will need read access to them.

FIXME: GeomVertexReader

Now that you know this, you can make your computer calculate the volume
of a mesh.


Session 12
----------

### Takeaway

A texture is the definition of a surface's properties. These properties
include color, normal, transparency, and others.


### Panda3D

`panda3d.core.Texture` manages discrete grids of data vectors. Think
"image that encodes information, maybe even an image."

In the context of this lecture, however, the term "texture" also refers
to the whole process, and the data that it consumes, that leads up to
the determination of properties which then are fed into the functions
that determine the actual appearance of a surface point.

The simplest typical process is that we provide a model with UV
coordinates on its vertices, and an image that these coordinates refer
to. After rasterizing the scene, we now have UV coordinates for each
surface point that we want to draw, and can interpolate the color value
from the provided image, and are done. More advanced workflows do also
look up further data that is provided in the same way, like normals,
roughness, etc., and feed them into functions that model the interaction
of light and surfaces.

A less typical, but equally valid approach would be to *not* provide an
image, but use the UV coordinates themselves as input for the function
that determines that coordinate's "texture". Examples for that are the
noise functions (Perlin, Worley, PSRD) that can be found [here](https://github.com/stegu/webgl-noise).


### Personal notes

In the early days of modern graphics cards, their functioning was
configured, not programmed. Developers were limited to choosing from the
set of functions that their cards provided.

The liberation from this began where a surface point's color in the
final output image is calculated. This is why programs running on the
GPU are called "shaders" today, no matter what they actually do; The
first shaders did what in the terminology of art is called shading.

Transparency on the GPU is a topic too full of difficult problems to be
discussed here.


Session 13
----------

Missing.


Session 14
----------

Windowing
Clipping
PBR / NPR
Object/Image space algorithms for occlusion
Painter's algorithm
...and then the sound cuts out.


### Panda3D

Windowing is left to the windowing system, that is what it is for.

Clipping happens automatically on the GPU. Backface culling also happens
there, unless you set the render attribute that makes your triangles
two-sided.

However, there is also a CPU-side culling process. FIXME

Z-buffer: FIXME


Session 15
----------

Student project presentations


Session 16
----------

# Panda3D

Implementing the fractals is left as an exercise to the reader. How
about a nice 3D Koch snowflake mesh generator, or a fragment shader for
the Mandelbrot set?

Image functions... FIXME: Would this be a good time to talk about
texture formats?


Session 17
----------

Same as 16???


Session 18
----------

We will not tackle raytracing here. Or shadows.

FIXME:
Lambertian diffusion
Flat shading
Gouraud shading
Phong shading


Session 19
----------

### Panda3D

FIXME: `Texture.get_ram_size()`

### Personal notes

In the grid with hexagonal cell borders, the centers of the cells form
a grid of triangles. This is the 2D case of a simplex grid. In practice,
it usually gets scaled a bit, so as to better fit into unit squares. For
a great explanation, please see the [PSRD noise tutorial](https://stegu.github.io/psrdnoise/2d-tutorial/2d-psrdnoise-tutorial-01.html).

When you sample the height of waves in the North sea, you get the
JONSWAP spectrum, and using Fast Fourier Transformation can be turned
back into realistic waves: [Part 1](https://www.youtube.com/watch?v=PH9q0HNBjT4), [Part 2](https://www.youtube.com/watch?v=yPfagLeUa7k)

This is just one example of the Fourier transformation bad habit of
popping up over and over again when you work with computers.


Session 20
----------

### Panda3D

NPR deserves a much larger space than I can afford it here.

This session dives into raytracing, which I said rather categorically
not to be rasterization. But let us consider though the case of an eye
ray that hits a surface, and would now use a shadow feeler to check
which lights illuminate it.

When using a rasterizer, we now can not just shoot another ray into the
scene to check for a collision between surface point and light. We can,
however, invert the idea, and implement shadows with it.

Let's say we have a spotlight in the scene. Since it already has a kind
of lens like a camera, we might as well render the scene from the
perspective of the camera. When we do so, we could get a color image
that we don't care about right now, but we would also get a depth map of
the scene, which represents how far into a scene the light shines. Now
when we render the scene from the perspective of the actual camera, we
can use the fragment's position to look up whether it was illuminated by
the spotlight.

FIXME: Code


### Personal notes

Radiosity: Probably used by modeling software to bake occlusion maps?
Bit beyond my horizon.


Session 21
----------

### Panda3D

Antialiasing as described here is but one technology of several that are
used to deal with the jaggies.

All the temporal sampling problems apply.


Session 22
----------

FIXME
* Panda3D history
* Panda3D sound system
* Level of Detail


Session 23
----------

Post-processing, FilterManager
Metrics also pop up in Search.
FIXME: Rewatch. Probably mention saving images, and processing them in
compute shaders.


Session 24
----------

`44:09`: Literature

We already dealt with animation [here](https://github.com/TheCheapestPixels/pandacademy/blob/IVC/geometric_modeling/geometric_modeling.md#bones).

Animations are also a wide field of study. FIXME: Provide examples, like Gears of War animation blending, neural networks controlling characters, ...


Session 25
----------

This is a very interesting and important topic which I will not comment
on here because it simply goes into the opposite direction of what you
would usually do with Panda3D.

### Personal notes

...except that mocap setups are absolutely essential in the production
of many games, so they are absolutely relevant to *using* Panda3D.
However I have nothing to add besides "`mediapipe` can do some cool 
stuff."


Session 26
----------

FIXME; Shapekey animation, boids


Session 27
----------

BDRF is the math that you put into a fragment shader to do PBR.
FIXME: Reflections; Show image-based reflection, mention SSR.


Session 28
----------

### Personal notes

The term "anatomy" here does not refer to the biological mechanism of
face muscles. As [Ekman explains](https://paulekman.medium.com/the-history-of-the-facial-action-coding-system-facs-8787a86ed81f),
anatomy textbooks were of little to his work, but that he found an old
French textbook on the anatomy (meaning, the structure) of the space of
facial expressions. While there is a correlation, there is also a layer
of abstraction here: Muscles activating creates the skin deformation
that is a facial expression, and the presence or absence of facial
expressions implies the activation level of the muscles. However for
most practical purposes, the biological anatomy does not have to be
worried about.

Thus, FACS is not an alternative to systems using FDP/FAPs, it *is* just
such a system when implemented to create facial animation. By itself it
is a method to transcribe facial expression to tuples of activation
unit, intensity, and duration. Also it was developed to systematically
research the impact of emotions on facial expressions, and thus does not
deal with things like e.g. tongue movement, which are relevant when
(re-)generating the animation state of a face from a stream of visemes.

"Smart objects": FIXME:
* `NodePath.*_tag` / `NodePath.*_python_tag`
* Storing behavior trees in objects
* Autonomous Virtual Characters: Mention `pychology`

One important aspect of making AVCs believable in the sense that they do
not break an observer's immersion in the simulation does not seem to be
to maximize their ability of making highly complex actions with extreme
realism, but to minimize the amount of nonsensical actions that they
make. To use the example of games: Players are surprisingly tolerant to
NPCs standing around all day, giving out the same quests over and over.
During an escort mission, the escortee running into a wall, or right
into groups of enemies, is absolutely not.

Groups of actors: FIXME: Boids

FIXME: OpenAL HRTF


Session 29
----------

Missing.


Session 30
----------

### Panda3D

Setting up red-blue and cross-eye stereoscopy (in the rendering sense,
not the perception one) in Panda3D is [absurdly easy](https://docs.panda3d.org/1.10/python/programming/rendering-process/stereo-display-regions).