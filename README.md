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
* [Courses](./courses.md): Terse explanations around lavishly commented
  programs, explaining the basics of modern realtime computer graphics,
  and how they are used in and through Panda3D.
* [Presentations slides](./presentations/presentations.md): Basically
  the target of a metaphorical cross-compilation from the
  above-mentioned courses to slide deck presentations.
* [Noise](./noise/noise.md): Notes on noise, e.g. Perlin, Worley, PSRD.
* [Papers and Talks](papers_and_talks.md): A collection of, and notes
  on, academic papers, blog posts, video presentations, and
  conference-style talks.
* [Other people's content](other_peoples_content.md): Lots of
  educational stuff that other people created.


TODO
----

* [ ] History: This is just a sketch.
* [ ] Courses: See there.
* [ ] Presentations: Just fragments so far.
* [ ] Noise: Working code, but that's it. This should become a course.
* [X] Papers and Talks: Basically a dumping ground in working condition.
      Further papers will be added as I discover them, notes on their
      content go into the "Paper Dissection" category, and as they form
      more fully rounded explanations of a topic (and get implemented),
      new courses to contain those topics can be created.

      As such, this document being in flux is its intended state.
* [ ] Paper Dissection: Totally unintegrated. As mentioned above, this
      is the mulch from which courses and code grow.
* [X] Other people's content: Another dumping ground.


NOTES
-----

* Advanced rendering techniques
  * PBR: Throw lots of optics-derived math at your lightning model.
    The current champion is the Disney's Principled BSDF.
    * Blender explaining the Principled BSDF: https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
    * Values for PBR artists: https://physicallybased.info/
  * SDR / HDR
    * SDR: Keep values in the [0.0, 1.0] range
    * HDR: Use open values for total intensity, then tonemap them.
  * [Unity's HDRP](https://forum.unity.com/proxy.php?image=https%3A%2F%2Fdocs.unity3d.com%2FPackages%2Fcom.unity.render-pipelines.high-definition%4010.2%2Fmanual%2Fimages%2FHDRP-frame-graph-diagram.png&hash=45c11349f9bb3a524fabfc91bcaf9f2e)
* Color
  * [CIE 1931 / XYZ](https://en.wikipedia.org/wiki/CIE_1931_color_space)
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
