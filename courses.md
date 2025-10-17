From (nearly) Zero to Game Dev Allrounder
=========================================

Few courses are complete yet, and neither is the list of courses itself
complete. As long as I do get the "onboarding Python developers to 
Panda3D" part done eventually, I am fully committing to scope creep, so
as to let you loose on the whole wide world of game development.


Preparatory Course
------------------

The courses after this one assume that you...
* understand basic Python (you don't need to know the whole standard
  library by heart, but sentences like "So we'll import a class from 
  this module, instantiate an object from it, and call these methods"
  should not scare you any more)
* can `pip install panda3d` (preferably in a virtualenv, but it's your
  system...)
* can verify that your system is running OpenGL 4.30 or higher (e.g. by
  running `glxinfo`)
* are not afraid of math. Computers are overgrown pocket calculators
  with ambitions, games model a lot of what they do in numbers and
  equations, and computer graphics in particular are one of the purest
  expressions of computing being mathematics in motion, so a basic
  (school-level) fluency in math will be necessary to get anywhere
  with anything.

These requirements are a bit harsh, contain interesting topics *should*
be explained here, as well as not containing other interesting topics
that should also be explained here; In particular:
- [ ] Math: Can't hurt to refresh our knowledge. FIXME: Sort through
      e.g. Khan Academy to find the relevant content.
- [ ] Python: There should be links to outside material like programming
      courses and installation guides. FIXME: Mention python.org docs,
      but also provide something else.
- [ ] [History](./history/history.md): The history of video games,
      computer graphics, and Panda3D.


Panda3D Basics
--------------

- [X] [Hello Panda3D](./hello_panda3d/hello_panda3d.md): Getting the
      basics out of the way. This is a quick onboarding to Panda3D that
      demonstrates:
      * Tasks and events, allowing you to structure your applications,
      * The scene graph, allowing you to structure your 3D scenes.
- [ ] [Scene Graph deep dive](./scene_graph/scene_graph.md): Everything
      to know about `NodePath`, as far as it concerns this course.
- [ ] [The CPU side of rendering](./cpu_rendering/cpu_rendering.md):
      Panda3D's rendering process. We explore how
      * Panda3D sets itself up for operation,
      * your scenes get turned into sequences of commands that are
        issued to your graphics card.


From (nearly) zero to knowing what rendering and shaders are all about
----------------------------------------------------------------------

A course on computer graphics. We will...
* use Panda3D to set up scenes, and the infrastructure to render them,
* explore the rendering process in enough detail to configure it and
  write shaders for it,
* get an overview of the major technologies from which rendering
  pipelines are pieced together.

- [ ] [Geometric Modeling](./geometric_modeling/geometric_modeling.md):
      A deeper look into meshes, textures, and animations. After this
      course, you will understand how the objects in your scene are
      represented as data. FIXME: lacks shapekeys
- [ ] [The GPU side of rendering](./gpu_rendering/gpu_rendering.md):
      This explains what happens when the rendering process hits
      the metal, and how we control it with shaders. It also explains
      compute shaders, with which we can leverage the graphics card's
      power for other tasks than rendering. FIXME: Closing in on being
      done in scope. Lacks images and code example integration.
- [ ] [Color: Physics-based Rendering (PBR)](./color/color.md): From
      Lambertian diffusion to all the effects. FIXME: Just notes so far.
- [ ] [Shadows](./shadow/shadow.md): Explains shadow maps. FIXME: Should
      also explain shadow volumes.
- [ ] [Light](./light/light.md): How to do (mostly) the same graphics
      with much less effort.
      FIXME: Subchapter on Tiled/Clustered/Volume is three links and a
      quick note, the one on Variable-Rate/Adaptive is not much better.
      Zero implementation.
- [ ] [Anti-aliasing](./antialiasing/antialiasing.md): Fighting jaggies.
      Also texture filtering.
- [ ] [Rendering pipelines](./rendering_pipelines/rendering_pipelines.md)
      FIXME: This needs to be renamed.
      FIXME: This is just loose notes on dealing with performance
      problems now; The rest has been absorbed into other chapters.


Cool Effects
------------

Second course on graphics, specifically how to achieve effects like
atmosphere, refraction, etc.; How to dip your toes into raytracing while
working with a rasterizing pipeline, I guess. Most of these effects will
probably composed in the rest of the image.
*[Noise](./noise/noise.md): Fundamental to *so much*.
  * Terrain
* Space partitioning
  * FIXME: SDF makes Tiled Shading more efficient, and BVH / octree is
    required for raymarching. So where to put it?
  * Topics
    * Spatial Hash
      * [bazhenovc's explanation](https://github.com/bazhenovc/SpatialIndex)
    * Octree
    * sparse voxel cone tracing (for global illumination?)
      * paper: https://research.nvidia.com/sites/default/files/publications/GIVoxels-pg2011-authors.pdf
      * nvidia: https://developer.download.nvidia.com/GTC/PDF/GTC2012/PresentationPDF/SB134-Voxel-Cone-Tracing-Octree-Real-Time-Illumination.pdf
      * Basic: https://simonstechblog.blogspot.com/2013/01/implementing-voxel-cone-tracing.html
      * Evaluation: https://www.diva-portal.org/smash/get/diva2:1886204/FULLTEXT01.pdf
      * Cascaded: https://www.gamedeveloper.com/programming/graphics-deep-dive-cascaded-voxel-cone-tracing-in-i-the-tomorrow-children-i-
      * Temporal: https://www.digipen.edu/sites/default/files/public/docs/theses/sanghyeok-hong-digipen-master-of-science-in-computer-science-thesis-temporal-voxel-cone-tracing-with-interleaved-sample-patterns.pdf
* Culling on Compute: https://vkguide.dev/docs/gpudriven/compute_culling/
* Texture Speedups
  * Transferring textures takes a lot of time.
  * [block compression, mipmap, virtual textures](https://www.youtube.com/watch?v=M3BSCH7oucc)
* Technology breakdowns for Unreal Engine 5 technology
  * [Nanite (virtualized geometry)](https://www.youtube.com/watch?v=TMorJX3Nj6U)
  * [Lumen (reflections and global illumination)](https://www.youtube.com/playlist?list=PL5sTHXdX47kh4e5MU11VPGw1MWpg3G51S)
* Color Spaces
  * OKLab: Great gradients
  * MixBox: Mixing colors like paint
* Raymarching
  * Basic Idea
  * Signed distance functions and distance fields
  * Atmosphere
  * Aurorae
* Particle systems
  * Fireworks
  * Boids
  * Physical systems
* Navier-Stokes for wind, clouds, and water
Other topics that should be dealt with:
* Tessellation and Geometry Shaders
* Task and Mesh Shaders (and how to get by with Compute Shaders)
* Maybe move shadow volumes here.
* Reverse depth buffering
* Bindless textures
* HDR
* Tonemapping
  * linear RGB, sRGB
  * https://www.khronos.org/news/archives/khronos-pbr-neutral-tone-mapper-released-for-true-to-life-color-rendering-of-3d-products



The Wider Field
---------------

FIXME: This is an incubator for game development courses in general.
Notes collected here should be spun off into their own courses as the
occasion arises. A good starting point may be to go over the collection
of papers.

* Procedural Generation: Infinite art assets for free.
* Sound: The other sense that Panda3D can stimulate.
* Game Balancing
* Art Direction
* Writing
