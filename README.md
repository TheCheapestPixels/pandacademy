Pandacademy
===========

Video game development is an absurdly wide field of study. It draws upon
several forms of art, a truly interdisciplinary study of sciences, and
brings it all together through software development. To master it in
fullness would require multiple lifetimes.

Video game development is also a field that getting involved with is
easier than ever before. Powerful tools are freely available.
Professional developers reveal all the latest tricks in GDC talks, and
content creators flood the Internet with information.

The purpose of this repository is to accrete knowledge about video game
development in terse form until it can be refactored into practical
courses and/or applications. This spans the gamut from basics of
graphics programming to the latest talks and research papers, and from
abstract theories to practical implementation, while leaving out the
full breath of knowledge, so as to give you an overview, then launch you
off to wherever you can continue your exploration. The point is to
provide a skeleton of knowledge as quickly as possible, which then can
be turned into expertise through self-guided further study and practice.

As these resources are written with a "Let's get things going already"
attitude, initial focus will be on the practical purpose of video game
development: To have running code that can be iterated upon until the
game is shippable. For this, the Python programming language, the
Panda3D engine, and GLSL will be used. The rationales are:
* Python is an easy to learn language that has proven itself in
  industry, science, and hobbyism, and which has a massive ecosystem.
* Panda3D is a 3D engine that is sufficiently comfortable to use, but
  does not hold your hand to a degree that it forces you into specific
  patterns of development. Especially with regard to graphics it is a
  surprisingly thin layer over OpenGL (or other graphics backends); It
  provides the tools that remove the tedium of working with it, but then
  let's us take over and deal with the nitty-gritty ourselves.
* GLSL is the Khronos standard for human-readable shading language.
* Panda3D is what brought the authors together.


### Status

Very new, very alpha. Basically this is a list of academic papers that
are (or seem to be) interesting, and a bunch of example code that begins
to congeal into a course on the basics of graphics programming. But it's
a starting point.


Content
-------

* [From (nearly) zero to knowing what rendering and shaders are all about](graphics_programming.md)
  A rough course on the basics of modern realtime computer graphics.
  Instead of loading models and textures from artist-created files like
  a sane person, we create them in code, so as to get to know the data
  structures involved. Then we take a look at how that data is processed
  on the GPU. We round it out with a look at the infrastructure that
  turns it all into a cohesive engine.
* [Papers and Talks](papers_and_talks.md): A collection of, and notes
  on, academic papers, blog posts, video presentations, and
  conference-style talks.


TODO
----

* [From (nearly) zero to knowing what rendering and shaders are all about](graphics_programming.md)
  needs to have its Panda3D-centric parts split out into its own
  courses.