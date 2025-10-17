Color
=====

Now that we know about shaders, we will start at fragment shading; We
have triangles on the screen, now they need coloration.


Non-Photorealistic Rendering (NPR)
----------------------------------

In the context of game development, the point of computer graphics is to
realize the intended aesthetics. If the answer is in the vicinity of
"photorealistic", then the way to go about it is Physics-Based
Rendering (PBR), which we will deal with in the next chapter. In fact,
even many graphics that do *not* look photorealistic in themselves do
use a PBR-based image as a start, and apply filters until the desired
look is achieved.

Thus, the answer to "What is NPR?" is "Anything besides or beyond PBR."
That in turn makes this chapter a catch-all for a bewildering variety of
technologies that can not possibly be enumerated here, and defy
categorization. In fact, most deal not just with shading fragments, but
involve design decisions all along the rendering pipeline.

For that reason, this chapter will just hit upon some topics to wet your
appetite.


### Object ID Buffer

Sometimes you need to know which object is where on the screen.
* Assign each object a unique number as their ID. This can be done as a
  vertex array column, or as a shader input.
* In the fragment shader, write that number as the output.

Now you can do things like...
* look up what object is right under the mouse pointer. As a side note,
  this is usually done more easily and efficiently by the collision
  system, shooting a ray starting at the camera (or its near plane) into
  the scene. But it *is* possible to answer with Object ID buffers as
  well, especially if you are already creating them for other purposes
  as well.
* silhouetting objects.


### Image Filters
### Cel shading

* Classical techniques
* Inverse hull mesh for outlines
* Guilty Gear Xrd


### Crosshatching

* Return of the Obra Dinn


Physics-Based Rendering (PBR)
-----------------------------

[LearnOpenGL article](https://learnopengl.com/PBR/Theory)
[PBR with Cook-Torrance](http://www.codinglabs.net/article_physically_based_rendering_cook_torrance.aspx)
[DylanCheetah's shader tutorials](https://github.com/Cybermals/panda3d-shader-tutorials)

* Diffuse reflection: Light shines on an object and is scattered out in
  all possible directions.
  * Lambertian reflectance: Outgoing light = incoming light times the
    cosine of the angle between Incident and Normal
* Specular Reflection: Light shines on a surface and is mirrored out.
* Fresnel equations
  * Describe the transmission and reflection of light at the interface
    between optical media.
  * Model light as a traversal wave.
  * Explains polarization.
* Schlick's approximation
  * The contribution of the Fresnel factor in the specular reflection of
    light from a non-conducting interface between two media.
* Trowbridge-Reitz GGX
  * Formula that was developed, forgotten, and reinvented:
    * ["Average irregularity representation of a rough surface for ray
      reflection"](https://pharr.org/matt/blog/images/average-irregularity-representation-of-a-rough-surface-for-ray-reflection.pdf)
    * ["Microfacet Models for Refraction through Rough Surfaces"](https://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf)
  * Microfacet distribution
* IES Light Profiles


Reflection
----------

There are several effects of which it can be said that they are what
makes an image "pop"; Reflections are definitely among those.

The problem with reflections is that they do not just involve the object
being rendered, the camera, and the lights, but also all objects in the
vicinity. Because of this, we have to do use tricks to achieve the
effect of reflection efficiently.


### Image-Based Lighting

We can simply put a camera inside our model, and render the entire
scene around it into a texture, specifically a cube map. Then, when
shading a fragment, we can use that cubemap to look up the reflection
into a certain direction.

The first drawback of this method is that we have now modeled the
reflector as a point. All relefctions will appear as if reflected from
the point where we put the camera, no matter where on the model they
actually occur.

Another drawback is that reflections of reflections will not be handled
well. FIXME: Because order of rendering of meshes.

A third drawback is that rendering the reflection map costs time in
itself. We have basically three options to adjust how much time we
spend, by deciding how often we do it:
* Every frame: Obviously, this is the most resource-hungry approach.
* Every few frames: Reflections will now occur in a stop-motion
  appearance. This approach makes sense when you do not have the frame
  budget to spare to update all reflection maps each frame, but also
  do not mind the stop-motion effect, so now you can update the
  reflection maps in a round-robin fashion.
* Once; This assumes that the environment around the mesh does not
  change, or does so in ways so small that it won't be obvious that a
  model has moved from place to place. In fact, if we reuse a scene's
  skybox, we do not need any separete reflection maps for our models at
  all.


* [GPU Gems](https://developer.nvidia.com/gpugems/gpugems/part-iii-materials/chapter-19-image-based-lighting)
* [Wikipedia](https://en.wikipedia.org/wiki/Image-based_lighting)
* [LearnOpenGL article on Diffuse](https://learnopengl.com/PBR/IBL/Diffuse-irradiance)
* [LearnOpenGL article on Specular](https://learnopengl.com/PBR/IBL/Specular-IBL)


### Screen Space Reflection (SSR)

What if we reflected only those parts of the scene that happen to be on
the screen themselves?


### Planar Reflection

A somewhat efficient approach for large, flat reflecting polygons, e.g.:
* water
* floors
* mirrored walls

Render the scene from a camera that is the main camera mirrored on the
surface. Use its output for the reflection terms.


### Raytracing

This approach is to knuckle down and do the hard work.
