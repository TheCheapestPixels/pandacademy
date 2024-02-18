From (nearly) zero to knowing what rendering and shaders are all about
======================================================================

This course assumes that you...
* can `pip install panda3d` (preferably in a virtualenv, but it's your
  system...)
* can verify that your system is running OpenGL 4.30 or higher (e.g. by
  running `glxinfo`)
* understand basic Python (you don't need to know the whole standard
  library by heart, but sentences like "So we'll import a class from 
  this module, instantiate an object from it, and call these methods on 
  the object" should not scare you any more)
* can imagine a linear projection of a 3D space into a 2D space.
* are not afraid of math. Computer graphics is one of the purest
  expressions of computing being mathematics in motion, so a basic
  fluency in several fields of math will be necessary to get anywhere
  with anything. Here we will mostly get away with `sin`, `cos`, and
  multiplying a matrix with a vector.

This course is also nowhere near complete yet. The planned curriculum
is:
- [X] Hello Panda3D: Getting the basics out of the way.
- [X] Procedural modeling and animation (TODO: lacks shapekeys)
- [ ] Rendering and shaders (needs refactoring and comments)
- [ ] A ShowBase-less Hello World to explain what is going on on top of
      all the rendering stuff


Hello Panda3D
-------------

A good first point of contact with the API is
[the Panda3D tutorial](https://docs.panda3d.org/1.10/python/introduction/tutorial/index).
Here we will speedrun the essentials, which may make the tutorial more
palatable, and/or let you dive right into the further course right here.
We will also use a terser coding style than the manual.


### Installation

`pip install panda3d`

TODO: dev version builds


### The smallest possible program

```python
from direct.showbase.ShowBase import ShowBase


ShowBase()
base.run()
```

Okay, confession time: This program does some weird stuff, and that I
have to say this about the very first and most basic Panda3D program
sure does not bode well.

For context: There are two modules in the Panda3D Python package:
* `panda3d` contains all the things that are implemented in C++, and
  wrapped with a Python API. If something is performance-critical, it
  should probably go here.
* `direct` contains tools implemented in Python, many of which build
  on `panda3d`. The code that speeds up development right up to enabling
  live coding lives here.

`ShowBase` is the central workhorse of most Panda3D applications, and
can be thought of as "The Engine". When you instantiate it, you will see
a window pop up which, right now, will be black. When running
`base.run()`, it will turn grey, as rendering now happens, and you are
staring into empty space where emptiness shows up in grey.

If you are using an IDE to code along, you will have noticed that it
freaks out at the mention of `base`, and maybe your brain did, too.
After all, where does *that* come from?

When `ShowBase` is instantiated, it stores a reference to itself in
`__builtins__` under the name `base`. `__builtins__` is where Python
keeps its built-in functions, constants, types, etc., e.g. `str`, `zip`,
`open`, `False`, `SyntaxError`. That means that after instantiation, we
can use `base` to refer to the object we just created, and do so from
any part of our application's code. On one hand, this leads to code that
is much easier to write and read, as we do not need to drag a reference
to it around in other ways. On the other, it means that we won't be
able to create a second or third instance of `ShowBase`. On the third
hand, people who have strongly ingrained notions about what constitutes
clean code have already stopped reading a while ago.


### A slightly more complex program

Let's have a quick word about the systems that I consider to be the glue
that keeps Panda3D programs together.

* `base.task_mgr`: Keeps a list of functions that get executed every
  frame, e.g. the render loop `igLoop`, the inputs-reading `dataLoop`,
  and the below-explained `eventManager`. You can `print(base.task_mgr)`
  to see the list of current tasks, and use
  `base.task_mgr.add(some_function, sort=number)` to add your own tasks.
  `base.run()` starts the event manager's loop through the tasks, while
  `base.task_mgr.stop()` stops it. TODO: When? After ending the task
  that calls the function, or do the frame's tasks all run before the
  exit?
* `base.messenger`: This object manages Panda3D's event system. With
  `base.messenger.toggle_verbose()` you can make it print all the events
  that it processes. It is tightly coupled with the class
  `DirectObject`, which provides the interface for accepting events, and
  can be used as a base class for game objects. Since `ShowBase` also
  inherits `DirectObject`, I will use that instead of creating
  extraneous objects.

  With `base.accept(event_name, function)` you can register functions to
  be called when a certain type of event is thrown system;
  `base.messenger.send(event_name)` enqueues a new event in the event
  queue, while the `eventManager` task pulls one event after the other
  from the queue until it is empty, dispatching each in turn to the
  registered callbacks.

With this in mind, we can write a slightly more complex program:
```python
from direct.showbase.ShowBase import ShowBase


ShowBase()
base.accept('escape', base.task_mgr.stop)
base.disable_mouse()
base.run()
```

The first new line obviously stops the task manager when `escape` is
pressed. The second disables the second idiosyncracy of Panda3D: By
default, you can control the camera with the mouse, but don't ask me
how, just build something new, for which you need to disable these
default controls; They were built by and for people who sat down at the
DISH CAVE and went right into experimenting with new amusement park
rides.

While we are at it, I might as well lose a word about the scene graph.
Everything that Panda3D renders (and a few things beyond) are
represented by different kinds of `PandaNode`s. These are wrapped into
`NodePath`s, which are arranged into a tree (or rather, a DAG) where the
nodes have a spatial relation to their parent (and store attributes on
how to render their content, and the subtree below them). Two node types
are `Camera` (which is just what it sounds like) and `Geom` (which
stores geometry).

`ShowBase` creates a basic scene graph at `base.render`, with a camera
at `base.cam`; You can get a printout of its structure with
`base.render.ls()`. A model we'll have to provide ourselves; Luckily yet
another thing that `ShowBase` creates is the asset loader, and also
Panda3D comes with a small library of models.

```python
from direct.showbase.ShowBase import ShowBase


ShowBase()
base.accept('escape', base.task_mgr.stop)
base.disable_mouse()
model = base.loader.load_model("models/smiley")
model.reparent_to(base.render)
base.cam.set_y(-10)
base.run()
```

Here we load a model, attach it to the root of the scene graph, then
move the default camera in that scene graph back by ten units. Running
this program, you should see a ball with a smiley face on it.


### Under the hood

Again, `ShowBase` does A LOT. Let's consider the bits between scene
graph on one side, and the graphics APIs on the other:
![Between scene graph and APIs](hello_panda3d/internals.png)

[Here is a program](hello_panda3d/internals.py) that sets it all up
without resorting to `ShowBase`.

Some presentations:
* [Scene Graph](hello_panda3d/scene_graph.pdf)
* [Graphics engine](hello_panda3d/graphics_engine.pdf)
(.odp source files are in the `hello_panda3d/` directory.)


### `render_frame` in detail

Rendering is a three step process:
* App
* Cull
* Draw

These steps can all be run sequentially (non-threaded), or distributed
onto two or three threads. While the end-to-end time for each frame is
still the same, doing so may increase the rate at which frames are
finished (if the total time that each frame takes to process exceeds the
frame budget). Part of `render_frame` is to wait for all thread to be
done with their current workload, and then to start the next batch. How
the three stages are combined into threads is the threading model.

`render_frame` does:
* Flush BamCache (because why *not* here?)
* `open_windows()`: Just that.
* Flip frames (if flipping on sync)
* Release RAM images of textures that were drawn in the previous frame
* `_app.do_frame()`: The actual work of the three stages.
  * engine->cull_to_bins(_cull): Culls (if the threading model separates
    Cull and Draw).
  * engine->cull_and_draw_together(_cdraw): Culls and draws (if the
    threading model combines them).
  * engine->draw_bins(_draw): Draws (again, if the threading model
    separates Cull and Draw).
  * engine->process_events(_window): Handles events caught by windows.
* `_pipeline.cycle()`: Pushes each thread's data onto the next one.
* `GeomVertexArrayData::lru_epoch()`: Informs all relevant LRU caches
  that evictions may be considered / performed now.
* Manage threads to wait for still-running ones, then begin next frame.


Procedural modeling and animation
---------------------------------

In this course we will deal with using code to create geometric models,
and animate them. We will not deal with advanced procedural generation
algorithms to create complex objects, only with the underlying API that
would also be used to turn such complex models into actual data that
Panda3D can work on.

Special thanks go to [Entikan](https://entikan.dimension.sh/) whose
trailblazing led to me developing these examples based on his code.


### geometry

Here we generate a static model purely in code, so as to see what is
going on under the hood. In
[`basic_model.py`](./geometry/basic_model.py) we learn
* how to define a table for vertices,
* how to fill it with data,
* how to add primitives, in particular triangles.

[`main.py`](./geometry/main.py) is mostly a convenience so that we can
actually look at something.


### pbr

Building on `geometry`, we discuss the properties of PBR-capable models
and their textures. [`pbr_model.py`](./pbr/pbr_model.py) shows
* what vertex columns a PBR model typically uses,
* what materials are and do,
* what information is encoded in textures, and how,
* how to procedurally generate images to load into textures.

There are three executable progrems this time, where
* [`main_no_pbr.py`](./pbr/main_no_pbr.py) shows how the model looks in
  the default renderer,
* [`main_simplepbr.py`](./pbr/main_simplepbr.py) uses Moguri's
  [`panda3d-simplepbr` package](https://github.com/Moguri/panda3d-simplepbr),
* and [`main_complexpbr.py`](./pbr/main_complexpbr.py) does the same for
  Simulan's
  [`panda3d-complexpbr` package](https://github.com/rayanalysis/panda3d-complexpbr).

The specific PBR pipelines are at this point maybe a bit of a
distraction; The important thing is that we now know how any model is
represented as data, and have seen a rather involved example of how that
data is laid out. Nonetheless, they serve as a nice example of what is
possible when you know what you are doing.


### bones

Also building on `geometry`, we create the model of a tentacle, and give
it a chain of bones to animate it around. As you will doubtlessly expect
by now, [`bones_model.py`](./bones/bones_model.py) does the same old
"Create a table, fill it with vertices, add triangles" song and dance,
while adding information to the vertices about which bones they should
consider for changing their apparent data while the model is being
animated.

There are four paradigms of animation that I am aware of, with advanced
procedural animation techniques building on those. There are
* Forward Kinematics, basically just setting bones to translations
  generated ad hoc in code, shown in
  [`main_control_joints.py`](./bones/main_control_joints.py),
* Skeletal animation, which is basically the same, using pre-recorded
  and usually artist-generated animations; Here we use
  [`main_mocap.py`](./bones/main_mocap.py) to record an animation using
  [rdb's](https://github.com/rdb/) [`mocap.py`](./bones/mocap.py), and
  play it back with [`main_animation.py`](./bones/main_animation.py),
* Inverse Kinematics, which is the reverse of Forward Kinematics, in
  that the code provides a target that a chain of bones should reach
  for, and leaves it to mathematical tools to move the bones within
  provided constraints so as to reach the target, demonstrated in
  [`main_inverse_kinematics.py`](./bones/main_inverse_kinematics.py)
  using [CCD-IK-Panda3D](https://github.com/Germanunkol/CCD-IK-Panda3D)
  by [germanunkol](https://github.com/Germanunkol/),
* and Physical Simulation, where we add information about a physical
  approximation of our model to simulate how it moves under the
  influence of gravity and collisions by using Panda3D's Bullet
  integration as in [`main_physics.py`](./bones/main_physics.py).

Again, these applications only serve to demonstrate what is possible;
The important information is how the model is set up.


Rendering and Shaders
---------------------

TODO: Full refactor. We have these files:
* [Minimal shader example](shaders/minimal/shader.py) demonstrates
  vertex and fragment shader. That is sufficient to explain the default
  shading pipeline, and show off first tricks.
* [All-stages example](shaders/all_stages/shader.py)
  * all five rendering shaders in action
  * hardware instancing.
* [Minimal compute shader](shaders/compute/main_basic_compute.py)
  * Writing textures
  * Texture-to-texture transformation
  * Extracting texture data from the GPU back to the `Texture` object.
* [Conway's Game of Life](shaders/compute/main_game_of_life.py)
  * Memory barrier
  * How to screw up:
    * Write back into the input texture. Race condition between
      workgroups result.
    * Don't load the Moore neighborhood. Performance evaporates.