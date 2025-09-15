Color
=====

Physics-Based Rendering
-----------------------

[LearnOpenGL article](https://learnopengl.com/PBR/Theory)

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
* Trowbridge-Reitz
  * "Average irregularity representation of a rough surface for ray
    reflection" https://pharr.org/matt/blog/images/average-irregularity-representation-of-a-rough-surface-for-ray-reflection.pdf
  * Introduces the microfacet distribution that the paper below
    reinvents and calls GGX.
* "Microfacet Models for Refraction through Rough Surfaces" https://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf
  * Introduces the name GGX (see above)


Reflection
----------

* cubemap of surroundings / Image-Based Lighting
  * [GPU Gems](https://developer.nvidia.com/gpugems/gpugems/part-iii-materials/chapter-19-image-based-lighting)
  * [Wikipedia](https://en.wikipedia.org/wiki/Image-based_lighting)
  * [LearnOpenGL article on Diffuse](https://learnopengl.com/PBR/IBL/Diffuse-irradiance)
  * [LearnOpenGL article on Specular](https://learnopengl.com/PBR/IBL/Specular-IBL)
* Screenspace Reflection
* Raytracing
