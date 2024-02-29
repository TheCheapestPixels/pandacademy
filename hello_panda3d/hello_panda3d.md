Hello Panda3D
-------------

A good first point of contact with the API is
[the Panda3D tutorial](https://docs.panda3d.org/1.10/python/introduction/tutorial/index).

Here we will speedrun the essentials, which may make the tutorial more
palatable, and/or let you dive right into the further courses right
here.

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
