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

[`main_basic.py`](./main_basic.py) shows how to get Panda3D ready to
work, and start that work.


### Tasks and events

Let's have a quick word about the systems that I consider to be the glue
that keeps Panda3D programs together.

* `base.task_mgr`: Keeps a list of functions that get executed every
  frame, in regular intervals, or once. For learning and debug purposes,
  you can get a print-out of the current task list with
  `print(base.task_mgr)`, and by default that is:
  ```plaintext
   Task                  sort  Functionality
  ----------------------------------------------------------------------
   resetPrevTransform     -51  Updates NodePaths; Their current
                               transformation becomes that of the last
			       frame.
   dataLoop               -50  Processes changes / events from outside
                               of Panda3D, like window movements or
			       input devices.
   eventManager             0  Dispatches events
   ivalLoop                20  Progresses Intervals
   collisionLoop           30  ShowBase's hook for a collision traverser
   garbageCollectStates    46  Run the arbage collector
   igLoop                  50  Rendering
   audioLoop               60  Audio
  ```
  (The `print`'s output has been edited and commented.)

  `base.run()` starts the loop through the chain, while
  `base.task_mgr.stop()` sets a flag which causes the task manager to
  stop the loop once the current run of the chain is finished.

  You can use `base.task_mgr.add(some_function, sort=number)` to add
  your own tasks. Those functions will receive the task object as their
  argument, plus extra arguments that you can specify when adding the
  task. They will have to return `task.cont` or a similar value, or they
  will be removed from the task chain after being run.

  For further details, see the [Panda3D manual](https://docs.panda3d.org/1.10/python/programming/tasks-and-events/tasks).

* `base.messenger`: This object manages Panda3D's event system. With
  `base.messenger.toggle_verbose()` you can make it print all the events
  that it processes. It is tightly coupled with the class
  `DirectObject`, which provides the interface for accepting events via
  callback functions, and can be used as a base class for game objects.
  Since `ShowBase` also inherits `DirectObject`, I will use that instead
  of creating extraneous `DirectObject`s.

  With `base.accept(event_name, function)` you can register functions to
  be called when a certain type of event is thrown system;
  `base.messenger.send(event_name)` enqueues a new event in the event
  queue, while the `eventManager` task pulls one event after the other
  from the queue until it is empty, dispatching each in turn to the
  registered callbacks.

With this in mind, we can write a slightly more complex program:
[`main_basic_2.py`](./main_basic_2.py). Again, for further details,
please refer to the [manual](https://docs.panda3d.org/1.10/python/programming/tasks-and-events/event-handlers).

(If you're just skimming: `base.disableMouse()` makes camera movement
programmable, instead of using default mouse-based controls.)


### Loader and scene graph

Now we have talked about much of the setup around that for which we are
actually here: Setting up a 3D scene, and rendering it. There are two
kinds of building block:
* Nodes: Everything that Panda3D renders (and quite a few things beyond
  that) are represented by classes that inherit `PandaNode`.
* Nodepaths: These are containers for nodes, and are arranged into a
  tree (or rather, a Directed Acyclic Graph (DAG); Each `NodePath` can
  have several parents, but no loops may occur) where the
  node(path)s
  * have a spatial relation to their parent, and
  * store attributes on how to render the scene graph from here on out,
    meaning that they affect the content of this `NodePath` and the
    subtree below it.

Two node types are `Camera` (which is just what it sounds like) and
`Geom` (which stores geometry, and is Panda3D slang for "a mesh").

`ShowBase` creates a basic scene graph at `base.render`, with a camera
at `base.cam`; You can get a printout of its structure with
`base.render.ls()`; In fact `.ls()` works on any `NodePath`.

A model though we will have to provide ourselves. In the next course we
will create them in code, but most of the time in practice we will load
artist-generated models from files. To do so, we will use `base.loader`,
which has methods to load models, textures, sounds, and so on.

Thus we arrive at [`main_basic_3.py`](./main_basic_2.py), where we load
a model, attach it to the root of the scene graph, then move the default
camera in that scene graph back by ten units. Running this program, you
should see a ball with a smiley face on it.
