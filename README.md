Pandacademy
===========

Video game development is an absurdly wide field of study. It draws upon
several forms of art, a truly interdisciplinary study of sciences, and
brings it all together through software development. To master it in
fullness would require multiple lifetimes.

Video game development is also a field that getting involved with is
easier than ever before. Powerful tools are freely available,
professional developers reveal all the latest tricks in GDC talks, and
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

For details, see the TODO list below.


Content
-------

* [History](./history.md)
* [Courses](./courses.md)
  A rough set of courses on the basics of modern realtime computer
  graphics.

  Instead of loading models and textures from artist-created files like
  a sane person, we create them in code, so as to get to know the data
  structures involved. Then we take a look at how that data is processed
  on the GPU. We round it out with a look at the infrastructure that
  turns it all into a cohesive engine.
* [Noise](noise.md): Notes on noise, e.g. Perlin, Worley, PSRD.
* [Papers and Talks](papers_and_talks.md): A collection of, and notes
  on, academic papers, blog posts, video presentations, and
  conference-style talks.
* [Other people's content](other_peoples_content.md): Lots of
  educational stuff that other people created.


TODO
----

* [ ] History: Sketches.
* [ ] Courses: See there.
* [ ] Noise: Working code, but that's it.
* [X] Papers and Talks: Basically a dumping ground in working condition.
* [X] Other people's content: Same.
* [ ] Paper Dissection: Totally unintegrated.
* [ ] Preparatory course on math and coding: Nothing so far


NOTES
-----

* Scene graph
  * Relative spatial arrangement of nodes
  * Render attributes
* Object basics
  * Geom is geometry + animation (what else?)
  * Texture is metadata plus ram image in VRAM
* Advanced rendering techniques
  * PBR: Throw lots of optics-derived math at your lightning model.
    The current champion is the Disney's Principled BSDF.
    * Blender explaining the Principled BSDF: https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
    * Values for PBR artists: https://physicallybased.info/
  * SDR / HDR
    * SDR: Keep values in the [0.0, 1.0] range
    * HDR: Use open values for total intensity, then tonemap them.
* Noise
  * https://github.com/stegu
  * https://github.com/tuxalin/procedural-tileable-shaders
* Shaders
  * https://thebookofshaders.com/
  * Sub-Surface Scattering: https://therealmjp.github.io/posts/sss-intro/
  * Multichannel Signed Distance Fields: https://github.com/Chlumsky/msdfgen
  * What are bank conflicts? (rather arcane performance optimization problem) https://developer.nvidia.cn/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda
* Profiling / debugging tools
  * RenderDoc: https://renderdoc.org/
  * https://gpuopen.com/rgp/
  * https://developer.nvidia.com/nsight-graphics
  * https://www.intel.com/content/www/us/en/developer/tools/graphics-performance-analyzers/download.html
  * https://www.cltracer.com/
* OpenGL / GLSL tutorials: https://www.opengl.org/sdk/docs/tutorials/
* Textbooks
  * https://learnopengl.com/
  * PBR textbook: https://pbr-book.org/4ed/contents
