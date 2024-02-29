Noise
=====

Pseudorandom noise is fundamental to a lot of procedural generation.


Code
----

[Panda3D code](noise/panda3d_noise.py) using
[a collection of GLSL noise functions](https://github.com/stegu/webgl-noise)
that includes Perlin, Worley, PSRD.

TODO: Prettify and comment.


Resources
---------

* [A student's course project](https://physbam.stanford.edu/cs448x/old/Procedural_Noise.html)
  documenting fundamentals of popular noises.
* [Periodic Simplex grid Rotating something noise with Derivates](https://stegu.github.io/psrdnoise/2d-tutorial/2d-psrdnoise-tutorial-01.html)
* [Generating noise with different power spectra laws](https://paulbourke.net/fractals/noise/)


### Generating noise textures

There are two ways to utilize noise for texture generation:
* Generate and store
* Generate in-situ