Shadow Maps
-----------

* Basic Shadow Map
  * From the perspective of the shadow-casting light, render the scene
    into the depth buffer.
  * When lighting a fragment, look up the light's depth buffer value at
    the coordinate in which the fragment would be. If the depth is
    smaller than the fragment's distance to the light, the fragment is
    in shadow, otherwise it is in the light.
  * Problem: "Shadow acne", patterns of shadow on meant-to-be-lit
    surfaces, is introduced, as the process is a numerical approximation
    based on the depth buffer's samples.
  * Problem: Aliasing
    * If a sufficiently large area of a scene is lit, and inspected up
      close, the resolution of the shadow map will begin to show through
      aliasing artifacts.
    * Increasing the resolution reduces the artifacts proportionally, at
      the cost of render time and an exploding memory consumption.
  * Problem: Hard edges. Rendering from the shadow-casting light's
    perspective has introduced the assumption that the light source is
    point-shaped. Therefore, the shadows lack a penumbra.
* Depth bias
  * Addresses shadow acne
  * By adding a bias to the sampled depth value, shadow-creating
    imprecision is overcome.
  * Problem: "Peter panning" is introduced: If a fragment should
    be in shadow, but is too close to the obscuring surface, it
    will be lit.
* Front-face culling
  * Addresses shadow acne
  * If the shadow caster renders backfaces, the problems on the lit
    surfaces disappear.
  * RESEARCH: Problem: Light acne on the backside, I guess?
* Percentage-Closer Filtering (PCF)
  * RESEARCH: https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows/chapter-11-shadow-map-antialiasing
* Cascading Shadow Maps (CSM)
  * Addresses aliasing.
  * [Very quiet video](https://www.youtube.com/watch?v=u0pk1LyLKYQ)
  * Increases the perceptable shadow map resolution.
  * The view frustrum is subdivided along the view axis.
  * Separate shadow maps are rendered to cover the different depth.
* Variance Shadow Maps (VSM)
  * Addresses hard edges.
  * Statistical approach to soft shadows.
  * RESEARCH: https://developer.nvidia.com/gpugems/gpugems3/part-ii-light-and-shadows/chapter-8-summed-area-variance-shadow-maps
* Moment Shadow Maps (MSM)
  * Builds on VSM


Shadow Volumes
--------------

FIXME: Meshes are extruded away from the shadow caster?
