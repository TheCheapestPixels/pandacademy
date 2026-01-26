Noise
=====

FIXME: This is basically "Well, there's this library..." and a few
loose notes.


### Generating noise textures

Pseudorandom noise is fundamental to a lot of procedural generation.

There are two ways to utilize noise for texture generation:
* Generate and store
* Generate in-situ

Underlying grids (in n dimensions):
* Cuboid: Like regular grid paper.
* Triangular: Like grid paper made from triangles (which in 2D is the Simplex).


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
* Interleaved Gradient Noise
  * [Interleaved Gradient Noise: A Different Kind of Low Discrepancy Sequence](https://blog.demofox.org/2022/01/01/interleaved-gradient-noise-a-different-kind-of-low-discrepancy-sequence/)
  * [Dithering part three – real world 2D quantization dithering](https://bartwronski.com/tag/interleaved-gradient-noise/)
