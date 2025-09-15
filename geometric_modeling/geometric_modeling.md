Creating Geometry
=================

In this course we will deal with using code to create geometric models,
and animate them, so as to get an understanding for the data structures
that we are working with. In practice, there are two sources for art
assets that we are working with here:
1) Artists. Since we have already loaded pre-made models, we have this
   aspect covered, and this course is a look under the hood of what the
   artist's programs did to create the model file.
2) Procedural generation. We will not deal with advanced procedural
   generation algorithms to create complex objects here, only with the
   underlying API that would also be used to turn such complex models
   into actual data that Panda3D can work on.

Special thanks go to [Entikan](https://entikan.dimension.sh/) whose
trailblazing led to me developing these examples based on his code.


Geometry
--------

Here we generate a static model purely in code, so as to see what is
going on under the hood. In
[`basic_model.py`](./geometry/basic_model.py) we learn
* how to define a table for vertices,
* how to fill it with data,
* how to add primitives, in particular triangles.

[`main.py`](./geometry/main.py) is mostly a convenience so that we can
actually look at something.


### PBR

This section is a short excurse into waters that we will dip our toes in
deeper later on. Since PBR is
* is a very popular use case,
* is a sufficiently complex use case to show how things scale up,
* uses textures, "the other kind of art asset",
we will take a glimpse at it here anyway.

The idea is that we load all relevant information about our model's
optical properties into its vertices and textures.
[`pbr_model.py`](./pbr/pbr_model.py) shows
* what vertex columns a PBR model typically uses,
* what materials are and do,
* what information is encoded in textures, and
* how to procedurally generate images to load into textures.

There are three executable programs this time, where
* [`main_no_pbr.py`](./pbr/main_no_pbr.py) shows how the model looks in
  the default renderer,
* [`main_simplepbr.py`](./pbr/main_simplepbr.py) uses Moguri's
  [`panda3d-simplepbr` package](https://github.com/Moguri/panda3d-simplepbr),
* and [`main_complexpbr.py`](./pbr/main_complexpbr.py) does the same for
  Simulan's
  [`panda3d-complexpbr` package](https://github.com/rayanalysis/panda3d-complexpbr).


Animation
---------

### Bones

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


### Shapekeys

FIXME
