IVC2Panda3D
===========

"Interactive Visual Computing" (IVC) is a course at the university of
Hamburg, created as a merger of "Computergrafik und Bildsynthese" (CGB)
and "Realtime Interactive Media" (RTIM).

Video recordings of the course are available at the university's
[Lecture2Go platform](https://lecture2go.uni-hamburg.de/en/l2go/-/get/v/14163). In German.


This document are my study notes; Their intent is twofold:
* To help me refresh and deepen my knowledge of the basics of computer
  graphics, so as to enable me to do a real deep dive into shaders,
* To create a supplement for the course for people who want to learn how
  to apply what they have learned in Panda3D, possibly to learn about
  Panda3D at the same time.


Session 1
---------

* `00:17:40`: Definition of the scientific field of computer graphics
  and the problems that it tackles (scene creation complexity /
  computational intensity for generating graphics, ambiguity for
  understanding).

  Graphical Data Processing deals with three types of scene description:
  * Semantic: e.g. natural language "Charlie feeds Snoopy", knowledge
    representation `(action 'feeds (feeder 'charlie) (feedee 'snoopy))`
  * Geometric: e.g. geometric primitives, their parameters, and spatial
    arrangement. In Panda3D, this is the Scene Graph built from
    `NodePaths` which contain `PandaNode`s like `GeomNode`, which
    contains mesh (and animation) data.
  * Iconic: e.g. `charlie_feeds_snoopy.png`, or an image on the screen.
    Panda3D: Framebuffer content.
  Transforming one representation into another is the task of the four
  fields of Graphical Data Processing:
  * Iconic to geometric: Image Processing / Pattern Recognition
  * Geometric to semantic: Image Understanding
  * Semantic to geometric: Visualization
  * Geometric to iconic: Graphical Data Processing again? We seem to be
    shadowing the name here. Anyway, this is what this course is about.
* `00:35:50`: We'll be working with digital models of
  * Images
  * Geometry
  * Radiometry: Interaction of matter and energy
  * Colors
  * Digitalization: Turning analog functions into digital data

Panda3D provides tools to create / load / save geometric scene
descriptions, and turn them into iconic representations. It also does a
whole bunch more that is not relevant right now for this course.

Homework: Install Panda3D and make sure that it is running.
[Here is the tutorial.](../hello_panda3d/hello_panda3d.md)


Session 2
---------

* `00:00:00`: Prelude, and talking about the practical project again.
* `00:06:08`: Resources:
  * [Lecture materials](http://kogs-www.informatik.uni-hamburg.de/~dreschle/teaching/Lehre/Lehre.html)
  * [Handouts](http://kogs-www.informatik.uni-hamburg.de/~dreschle/informatik/Skripte/IVCHandouts.pdf)
* `00:07:05`: Literature
* `00:10:42`: There are classes of coordinate systems (e.g. cartesian,
  polar). Within each class there are types that define e.g. the
  relative arrangement of axes, directions of rotation, how vectors and
  matrices represent either, and how many dimensions are used. Instances
  of coordinate systems can be put into relation with one another
  mathematically, creating hierarchies. 
* `00:18:37`: There are four basic types of transformation:
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
  * E.g.: For 2D coordinates we use `(x y 1)` vectors and multiply with
    `((a b 0) (c d 0) (e f 1))` matrices. Note that when multiplying,
    the last column goes `0*x + 0*y + 1*1 = 1`, so the result is in
    homogenous coordinates again. In the other columns, the vector's `1`
    gets multiplied with `e` and `f`, so `(e f)` is the translation that
    is added "after" the operations in the `(a b) (c d)` square.
  Multiplying the matrices means concatenating the operations that they
  represent, and multiplying a vector with the matrix means transforming
  it through all those operations.

  The matrices are derived from definition and trigonometry for 2D in
  the lecture.
* `00:51:09`: 3D coordinate systems, handedness, examples in POVRay,
* `01:09:43`: `clock` variable
* `01:12:51`: POVRay geometric primitives
* `01:24:54`: `while` loop, and further POVRay syntax


Panda3D: The coordinate system's style can be configured, but the
default is Palm-Up Righthanded:
* x to the right
* y forward
* z up
* Pitch turns around x
* Roll turns around y
* Yaw is called heading, and turns around z
* Positions are in `xyz` order, but rotations in `hpr` order,
  meaning that they turn around axes `zxy`. Why? Probably usability.

Each `NodePath` contains the transformation between the `PandaNode` of
its parent and its own.

Model / View / Projection matrix and their combinations are available as
[shader inputs](https://docs.panda3d.org/1.10/python/programming/shaders/list-of-glsl-inputs#uniform-shader-inputs):
```glsl
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ViewProjectionMatrix;
```

```python
from panda3d.core import NodePath


parent = NodePath("Root of the scene graph")
child = parent.attach_new_node("Child node")
child.set_pos(2, 3, 4)  # Translation in x, y, z units
print(child.get_mat())  # Shows the transformation matrix' contents
child.set_hpr(90, 45, -50)  # Rotation in degree
FIXME: Scaling, shearing doesn't exist, sow the matrix.
```

Graphics Processing Units (GPUs, the CPU equivalent of a graphics card)
contains lots of matrix processing circuits that run in parallel.


Session 3a
----------

* `00:00:00`: Where were we?
* `00:12:25`: More about applying coordinate transformations and the
  hierarchy of coordinate systems.
* `00:25:38`: Using hierarchical transformations to build a snow man /
   recursive pyramid / Russian nesting doll / ammonite / etc.
* `00:53:50`: POVRay


Session 3b
----------

* `00:00:00`: Overview of topics to come:
  * Geometric modeling
  * Graphical algorithms
  * Photometric modeling

  Panda3D:
  * [Geometric modeling](https://github.com/TheCheapestPixels/pandacademy/blob/master/graphics_programming.md#procedural-modeling-and-animation)
* `00:07:52`: Motivation: What use is it?
* `00:37:09`: Geometric Modeling: How do represent an object as data?
  * Volume based
    * octree: Recursively splitting a cube into eight cubes
    * CSG: Set operations to combine primitives
  * Surface based: Next week

Panda3D: Octrees are not just for saying whether an object is or isn't
there. Each leaf of the tree can contain a reference to arbitrary data.
In that form, they can also be used as a simple space partitioning
algorithm, and speed up many other algorithms,


Session 4: Projections
----------------------

* `00:00:00`: Projections are transformations from one coordinate space
  into another, here in practice only planar 3D into 2D. Starting with
  distinguishing between parallel and central projection, lots of
  projections are derived.

  Panda3D: Camera position and near/far plane. FIXME: Code example,
  net transformation, reprojection of image coordinate.
  `.get_relative_*` here, too?


Session 5: Geometric modeling
-----------------------------

We'll model our geometry by defining
* vertices: Points of data
  * `vertex`: position
  * `texcoord`: UV coordinates of a texture at this point
  * `normal`: Normal vector for this vertex
  * etc.
* primitives:
  * Points:
  * Lines:
  * Triangles:
Points and lines may or may not be supported by any given GPU, and if
they are, support may be lackluster (like e.g. line thickness being
ignored).


`LineSegs` and `CardMaker`
Also `Intervals`.


Session 6
---------

* `00:00:00`: Projections revisited
* `00:11:06`: Illusions
* `00:32:56`: Lens Camera, depth of field
* `00:46:49`: POVRay cameras
* `01:00:24`: Front plane, back plane
* `01:03:42`: Higher-dimensional spaces

Yes, we can have depth of field, chromatic aberration, and all the
inaccuracies and effects of natural cameras, but we will have to fake
and approximate.

Front / back plane are called near / far plane in Panda3D.
FIXME: Lens types?

Higher-than-3-dimensional spaces are not supported by Panda3D; You will
have to come up with a way to represent your scenes and project them
into the scene graph yourself. If you can do so in shaders, I would like
to know how.


Session 7
---------

* `00:00:00`: Repetition, and further parametric functions and surfaces
* `01:20:54`: Topology

This lecture is of interest for libraries that generate models and
textures, and also for tessellation shaders.

More on splines: ["The Continuity of Splines"](https://www.youtube.com/watch?v=jvPPXbo87ds)

There is nothing about topology in Panda3D.


Session 8
---------

Panda3D light sources are pretty much equivalent to the POVRay ones.
However, they will not cast shadows by default.
FIXME: Types of light sources

There are no volume light sources (without raytracing).

Refraction effects need to be faked. Keep the math in mind, it will be
helpful when we write fragment shaders, or calculate the color of
blackbody lights.


Session 9
---------

FIXME: The experiment with the rotating disc of spectral colors. BEWARE:
The Pokemon epilepsy signal is a thing that exists.

For the topology part, there is again no direct applicability.


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

* `00:00:00`: Topology
* `00:09:03`: Notes on the graphical representation of objects
* `00:14:36`: Graphics algorithms

The algorithms in this lecture may become interesting in specific
problems, but aren't of immediate applicability.


Session 12
----------

* `00:00:00`: Practical experiments
* `00:01:30`: Color systems repetition
* `00:02:51`: Physiology of sight
* `00:00:00`:
* `00:00:00`:
* `00:00:00`:
* `00:00:00`:
* `00:00:00`:
* `00:00:00`:
* `00:00:00`:
