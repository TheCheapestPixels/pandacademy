Anti-Aliasing
-------------

The pixelated nature of computer-generated images gives rise to the
"jaggies", steps-like artifacts at the edges of triangles. There are a
lot of approaches to deal with them.


### Super-sampling AA (SSAA)

During rasterization, by default only one fragment is generated per
pixel, and it is sampled at the center of the pixel. However, the
rasterizer can be made to sample multiple points per pixel, and the
outputs of the resulting fragments can be blended into a final output.
Basically, we are rendering at a higher resolution, then scaling the
result down.
* This is supported by GPUs in hardware.
* Problem: The performance cost may be prohibitive.
* Problem: This is incompatible with Deferred Shading. A similar result
  could be created by increasing the G-buffer size, but that too is
  likely to increase memory footprint and bandwidth cost prohibitively.


### Multi-sampling AA (MSAA)

To improve on the performance of SSAA, we can depth-sample each pixel
multiple times, and for each triangle thus sampled, we fragment shade it
once per pixel. Usually this will result in only one fragment shading
per pixel.
* Also supported by GPUs in hardware.
* Problem: Also incompatible with Deferred Shading.


### Morphological AA (MLAA)

["Morphological Antialiasing", Alexander Reshetov, 2009](https://www.cs.cmu.edu/afs/cs/academic/class/15869-f11/www/readings/reshetov09_mlaa.pdf)
[Slides that provide a good summary](https://www.highperformancegraphics.org/wp-content/uploads/2017/Retrospective/HPG2017_Reshetov_MLAARetrospective.pdf)

* Find silhouettes, and the horizontal / vertical lines they consist of.
* Approximate them with slanted lines.
* Pixels that the slanted lines pass through get blended with their
  neighbors.

This approach works on all images.


### Fast Approximate AA (FXAA)

[Original paper](https://developer.download.nvidia.com/assets/gamedev/files/sdk/11/FXAA_WhitePaper.pdf)
An evolution of MLAA.

* Luminance Data: Either the rendering provides it, or we approximate it
  from the input image.
* High Pass Filter over the luminance data finds pixels with high
  contrast to their neighbors. We only process these.
* Approximate edges based on contrast data, and find a factor by how
  much to blend a pixel perpendicular to that edge.
* Analyze each pixel's 8-neighborhood to calculate a blend factor.
* Search edges for their full length, calculating a second blend
  direction and factor for the pixel.
* Choose blend direction, and blend by the hiher blend factor.


### Sub-pixel Morphological AA (SMAA)

[Original paper](https://www.iryoku.com/smaa/downloads/SMAA-Enhanced-Subpixel-Morphological-Antialiasing.pdf)
Another evolution of MLAA


### Temporal AA (TAA)

* [A paper giving an overview over the whole family](https://leiy.cc/publications/TAA/TemporalAA.pdf)


### TXAA

TAA with FXAA bolted on.


### Deep Learning AA / Super-Sampling (DLAA / DLSS)

nvidida uses neural networks.
