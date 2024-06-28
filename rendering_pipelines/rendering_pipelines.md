Rendering Pipelines
===================

How to render less
------------------

### Level of Detail to reduce triangle count
### Imposters
### Hardware Instancing

Tell the GPU to draw lots of copies of an object at the same time.
Problematic with transparency.


How to cut down on the number of light calculations
---------------------------------------------------

What we have been working with so far is "Forward Shading", which is the
simple approach that Just Works. Sadly it is also rather inefficient
with the GPU's resources when compared to what can be achieved if one is
willing to face a whole lot of problems when trying to be clever.


### Z Prepass

[video](https://www.youtube.com/watch?v=2ZK527cQbeo) for reference.

Overdraw is the inefficiency of shading a fragment that does not appear
on the final image. To reduce that waste, we can:

1. Render the scene only to the depth buffer. To do so, we use a vertex
   shader that cares only about a vertexes position. The fragment
   shader is best left unbound, but since that is currently not possible
   in Panda3D, we simply do not write to`gl_FragDepth`.
2. Render the scene normally with an `GL_LEQUAL` depth test.

Now only fragments that are at the visible surface are passed on to
fragment shading; Overdraw is zero. The performance tradeoff is that we
are running the vertex shader twice.

We can scale between these extremes by selecting a subset of the objects
to draw during the prepass. The denser an object's vertices are on the
screen, the less likely is it that its fragment shading cost outweighs
its vertex shading cost.

We can also use special meshes in the draw prepass that
* have only vertex positions, reducing memory bandwidth use
* are low-poly, They must be wholly contained in their full-quality
  counterparts at any time.

If we do *not* use special meshes, and the prepass thus is exact,
algorithms that depend only on the depth buffer can begin working at the
same time as the render pass.

FIXME: I'm also pretty sure that this doesn't work for transparency *at
all*.


### Deferred Shading

Rendering happens in two passes again, but very different from before.

1. Geometry pass: We forward-render the scene, but instead of doing
   light calculations in the fragment shader, we simply write the
   interpolated texture data (in screen space) into the G-bufeer
   (geometry buffer; just a buffer with lots of planes). Thus, we do not
   have to consider any light at all.
2. Lighting pass: We render a screen-sized quad with the G-buffer as its
   texture, so the vertex shader has to process only four vertices, and
   the rasterizer two triangles. In the fragment shader, we now have all
   the information from the G-buffer, can apply lighting calculations,
   and write the final fragment color.

Overdraw still happens in the first pass, but matters less.

Deferred Shading can't produce transparency.


### Hybrids: Saving transparency.

FIXME: This section is off the top of my head.
The approaches of Z Prepass and Deferred Shading only work on the
closest visible surface, and do not generate fragments behind it;
Objects that they work on can't be transparent. To deal with that,
transparent meshes are usually rendered in a separate transparency pass,
and the resulting image is composed into the one with opaque objects
thereafter.


How to reduce the number of lights to consider
----------------------------------------------

Usually there is a part in the fragment shader that is run once per
light in the scene. This number can be significantly reduced by using a
data structure that can determine quickly the set of lights that are
significant for a given fragment.

FIXME: Requires knowledge of space partitioning


### Tiled Shading

We subdivide the screen space into tiles, which represent a sheared
frustum within the camera frustum.


### Clustered Shading

The 3D equivalent to Tiled's 2D.


How to reduce the resolution of shadow maps
-------------------------------------------

### Cascaded Shadow Maps

[Very quiet video](https://www.youtube.com/watch?v=u0pk1LyLKYQ)
