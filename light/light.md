Light
=====

Probably slightly counterintuitively, this course deals with the
question of how to *not* calculate lighting information. More
specifically, calculating the effect that a group of lights has on a
fragment can be expensive, depending on how many fragments per final
pixel we shade, and how many lights may affect it. Therefore, to allow
for scenes with as many lights as possible, we need to minimize the
effort that we put into each fragment.


Reducing overdraw
-----------------

### Forward Shading

Assuming that we use the basic rendering pipeline, we are doing Forward
Shading. This means that we will
* render each object one by one,
* process each vertex in the vertex shader,
* rasterize the resulting faces,
* calculate the depth and color of each resulting fragment in the
  fragment shader,
* apply the Z test and transparency calculations.

That in turn means that we sink a lot of computing effort into fragments
that will not even appear in the final image; These are called the
"overdraw".


### Deferred Shading

We can address the overdraw by deferring the calculations involving
light until after it has been determined which fragments are visible.

We assume that all objects are opaque.

Rendering happens in two passes:
1. Geometry pass: We forward-render the scene. Instead of using the
   texture data in the fragment shader to calculate the fragment's
   color, we write it all into the G-buffer ("geometry buffer"; a
   framebuffer with planes corresponding to the textures that the meshes
   use). Thus, we do not have to consider any light at all.
2. Lighting pass: We render a screen-sized quad with the G-buffer as its
   texture, so the vertex shader has to process only four vertices, and
   the rasterizer two triangles. In the fragment shader, we now have all
   the information from the G-buffer, can apply lighting calculations,
   and write the final fragment color.

Overdraw still happens in the first pass, but does not entail the
lighting calculations.

However, there are also drawbacks:
* Deferred Shading can't produce transparency.
* The G-Buffer has a memory footprint; I a typical PBR workflow, it has
  12 channels. At Full HD resolution (1080p, 1920 x 1080 pixel) and at
  32 bit per channel, that means nearly 95 megabyte.
* Additionally, the whole G-buffer gets written, possibly multiple
  times, during the geometry pass, and read wholly once in the lighting
  pass. Thus there is a higher mamory bandwidth cost than with forward
  shading, which may outweigh the benefit of the decreased overdraw.


### Hybrid Shading

The lack of support for transparency in deferred shading can be
addressed by rendering the scene twice:
1. A deferred shading pass renders all opaque objects.
2. A forward shading pass renders all transparent objects, and composits
   it with the result of the first pass.

This results in a balance of all the advantages and drawbacks of the two
techniques.


### Early Depth Test

Another approach to combat overdraw is to do depth testing before
fragment shading. In general, a fragment shader can write to the output
`gl_FragDepth`, changing its apparent depth, and thus influencing the
decision whether it will be discarded or not during the depth test that
follows fragment shading.

However, many graphics cards have an interesting quirk called "early Z 
test" that reduces the fragment shading on the overdraw. If
* there is no fragment shader to begin with (as of September 2025,
  currently not possible in Panda3D),
* or if the fragment shader just does not write to `gl_FragDepth`, and
  instead lets the pipeline use the value that the rasterizer came up
  with,
* or the option is forced, in which case writes to `gl_FragDepth` are
  simply ignored,
then the depth test happens before the fragment shader is invoked. If
the fragment is discarded, then the fragment shader simply does not get
invoked.

It is, however, possible that a later fragment draws over the previous
fragment. This approach reduces overdraw, it does not eliminate it, and
it is an optimization that will usually *just happen*.


### Z Prepass

Building on the idea of the Early Depth Test, Z Prepass reduces the
overdraw even further by drawing the scene twice.

1. Z Prepass: We render the opaque parts of the scene only into the
   depth buffer; Our fragment shader does *nothing*.
2. Render pass: We render the scene again, using the depth buffer that
   we just created instead of a blank one. Now every fragment is
   compared against the opaque background of our view, and discarded
   before shading if it is behind it.

During the first pass, the cost of fragment shading is basically zero,
so the incurred cost is that of running the vertex shader twice.

As the density of vertices on the screen increases, this may outweigh
the payoff of the overdraw during the second pass being zero. This can
be addressed by using special meshes in the draw prepass that
* have only vertex positions, reducing memory bandwidth use
* are low-poly; They must be wholly contained in their full-quality
  counterparts at any time.

If we do *not* use special meshes, and the prepass thus is exact,
algorithms that depend only on the depth buffer can begin working at the
same time as the render pass.


Why even shade every fragment?
------------------------------

### Variable-Rate Shading

After rasterization, instead of shading each fragment, we shade the center of tiles sized 1x1, 1x2, 2x1, 2x2, 4x2, etc., and apply that color to
all fragments of the triangle.


### Adaptive Shading

Shade only every fourth pixel in every fourth row (numbers may vary).
Fill in the rest in a diamond-square pattern. If the four bordering
samples of a pixel are sufficiently similar, skip shading and just use
their average; If they are dissimilar, shade properly.

* This may cut down the ratio of actual shading done to half of the
  image.
* High-frequency details may get lost.


Cutting down the number of lights to consider
---------------------------------------------

Usually there is a part in the fragment shader that is run once per
light in the scene. However, a scene may contain a great number of
lights, slowing down rendering unacceptably.

The number of lights that have to be considered per fragment can be
significantly reduced by using a data structure that can determine
quickly which set of lights is significant for the fragment. This is
called "light assignment".

[Relevant blog post](https://wickedengine.net/2018/01/optimizing-tile-based-light-culling/); Note the links, too.


### Tiled Shading

[Paper by Ola Olsson, Ulf Assarsson, 2011](https://www.cse.chalmers.se/~uffe/tiled_shading_preprint.pdf)
* We subdivide the screen space into tiles, which represent a sheared
  frustum within the camera frustum.
* We render geometry representing a light's volume.
* For each tile that is at least partially covered by the light, we append the light's ID to that tile's list.
* When lighting a fragment, we find the tile ID, then the light list.


### Clustered Shading

[Paper by Ola Olsson, Markus Billeter, and Ulf Assarsson, 2012](https://www.cse.chalmers.se/~uffe/clustered_shading_preprint.pdf)
[Presentation by Ola Olsson](https://www.youtube.com/watch?v=uEtI7JRBVXk)


### Volume Tiled Shading

The 3D equivalent to Tiled's 2D.
