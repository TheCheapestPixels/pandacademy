From (nearly) Zero to Game Dev Allrounder
=========================================

Few courses are complete yet, and neither is the list of courses itself
complete. As long as I do get the "onboarding Python developers to 
Panda3D" part done eventually, I am fully committing to scope creep, so
as to let you loose one the whole wide world of game development.


Preparatory Course
------------------

The graphics courses assume that you...
* understand basic Python (you don't need to know the whole standard
  library by heart, but sentences like "So we'll import a class from 
  this module, instantiate an object from it, and call these methods"
  should not scare you any more)
* can verify that your system is running OpenGL 4.30 or higher (e.g. by
  running `glxinfo`)
* are not afraid of math. Computer graphics is one of the purest
  expressions of computing being mathematics in motion, so a basic
  fluency in several fields of math will be necessary to get anywhere
  with anything. For a start though, we will mostly get away with `sin`,
  `cos`, and multiplying a matrix with a vector.
* can `pip install panda3d` (preferably in a virtualenv, but it's your
  system...)

These requirements are a bit harsh, contain interesting topics *should*
be explained here, as well as not containing other interesting topics
that should also be explained here; In particular:
- [ ] History: How Panda3D came about, and what it was used for.
- [ ] Math: Can't hurt to refresh our knowledge.
- [ ] Python: There should be links to outside material like programming
      courses and installation guides.
- [X] [Hello Panda3D](hello_panda3d/hello_panda3d.md): Getting the
      basics out of the way. This is a quick onboarding to Panda3D that
      demonstrates:
      * Tasks and events, allowing you to structure your applications,
      * The scene graph, allowing you to structure your 3D scenes.


From Data to Image
------------------

A course on computer graphics.

- [ ] Scene Graph deep dive: Everything to know about `NodePath`, as
      far as it concerns this course.
- [ ] [Geometric Modeling](./geometric_modeling/geometric_modeling.md):
      A deeper look into meshes, animations, and textures. After this
      course, you will understand how the objects in your scene are
      represented as data. FIXME: lacks shapekeys
- [ ] [The CPU side of rendering](./cpu_rendering/cpu_rendering.md):
      Panda3D's rendering process. We explore how
      * Panda3D sets itself up for operation,
      * your scenes get turned into sequences of commands that are
        issued to your graphics card.
- [ ] [The GPU side of rendering](./gpu_rendering/gpu_rendering.md):
      This explains what happens when the rendering process hits
      the metal, and how we control it with shaders. It also explains
      compute shaders, with which we can leverage the graphics card's
      power for other tasks than rendering. FIXME: Also in the process
      of being written...
- [ ] [Color: Physics-based Rendering (PBR)](./color/color.md): From
      Lambertian diffusion to all the effects. FIXME: Just notes so far.
- [ ] [Shadows](./shadow/shadow.md): Explains shadow maps and, hopefully
      eventually, shadow volumes. See also
      [papers](./papers_and_talks.md#Graphics).
- [ ] [Light](./light/light.md): How to do (mostly) the same graphics
      with much less effort.
      FIXME: Subchapter on Tiled/Clustered/Volume is three links and a
      quick note, the one on Variable-Rate/Adaptive is not much better.
      Zero implementation.
- [ ] [Anti-aliasing](./antialiasing/antialiasing.md): Fighting jaggies.
- [ ] [Rendering pipelines](./rendering_pipelines/rendering_pipelines.md)
      FIXME: This needs to be renamed.
      FIXME: This is just loose notes on dealing with performance
      problems now; The rest has been absorbed into other chapters.
- [ ] Space partitioning: Octree and all the rest. FIXME: This has
      become relevant in earlier chapters.


Cool Effects
------------

Second course on graphics, specifically how to achieve effects like
atmosphere, refraction, etc.; How to dip your toes into raytracing while
working with a rasterizing pipeline, I guess. Most of these effects will
probably composed in the rest of the image.
* Raymarching
  * Basic Idea
  * Signed distance functions and distance fields
  * Atmosphere
  * Aurorae
* Particle systems
* Navier-Stokes for wind, clouds, and water


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
