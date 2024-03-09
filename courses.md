From (nearly) zero to knowing what rendering and shaders are all about
======================================================================

These courses assume that you...
* understand basic Python (you don't need to know the whole standard
  library by heart, but sentences like "So we'll import a class from 
  this module, instantiate an object from it, and call these methods"
  should not scare you any more)
* can `pip install panda3d` (preferably in a virtualenv, but it's your
  system...)
* can verify that your system is running OpenGL 4.30 or higher (e.g. by
  running `glxinfo`)
* are not afraid of math. Computer graphics is one of the purest
  expressions of computing being mathematics in motion, so a basic
  fluency in several fields of math will be necessary to get anywhere
  with anything. For a start though, we will mostly get away with `sin`,
  `cos`, and multiplying a matrix with a vector.

Few courses are complete yet, and neither is the list of courses itself
complete. As long as I do get the "onboarding Python developers to 
Panda3D" part done eventually, I am fully committing to scope creep, so
as to let you loose one the whole wide world of game development.

- [ ] Preparatory courses: The requirements above are a bit harsh, and
      contain interesting topics that *should* be explained here; In
      particular:
      * Links to outside material like programming courses and
        installation guides
      * Math, applied in Panda3D
- [X] [Hello Panda3D](hello_panda3d/hello_panda3d.md): Getting the
      basics out of the way. This is a quick onboarding to Panda3D that
      demonstrates:
      * Tasks and events, allowing you to structure your applications,
      * The scene graph, allowing you to structure your 3D scenes.
- [ ] Scene Graph deep dive: Everything to know about `NodePath`.
- [ ] [Geometric Modeling](./geometric_modeling/geometric_modeling.md):
      A deeper look into meshes, animations, and textures. After this
      course, you will understand how the objects in your scene are
      represented as data.
      
      TODO: lacks shapekeys
- [ ] [The CPU side of rendering](./cpu_rendering/cpu_rendering.md):
      Panda3D's rendering process. We explore how
      * Panda3D sets itself up for operation,
      * your scenes get turned into sequences of commands that are
        issued to your graphics card.
- [ ] [The GPU side of rendering](./gpu_rendering/gpu_rendering.md):
      This explains what happens when the rendering process hits
      the metal, and how we control it with shaders.
      
      TODO: Full refactor.
- [ ] The science of light and color: Physics-based Rendering (PBR),
      from Lambertian diffusion to all the effects
- [ ] Rendering pipelines
      * How to cut down on the number of light calculations:
        * Forward Shading: The unoptimized default.
        * Deferred Shading: Render object parameters to texture, then
          light those. `O(m+n)` is better than `O(m*n)`, and overdraw
          matterss less. Can't do transparency.
        * Hybrids: Saving transparency.
      * How to reduce the number of lights to consider (repuires
        knowledge of space partitioning):
        * Tiled Shading: For each tile on the screen, consider which
          lights affect it.
        * Voxelized Shading: The 3D equivalent to Tiled's 2D.
      * Light and shadow:
        * Mention drop shadows for historical reasons.
        * Simple shadowmapping
        * PSSM
	* There are further quality improvements, see the [papers](./papers_and_talks.md#Graphics)
- [ ] Space partitioning: Octree and all the rest.