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
