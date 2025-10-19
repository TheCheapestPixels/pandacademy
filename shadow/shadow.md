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

Footnote: We have assumed so far that each light has a shadow caster
(frustum). This one-to-one relationship is not necessary, and breaking
it allows for multiple similar lights to use the same shadow caster. A
possibility for further research would be to LOD those shadow casters,
splitting each into two and blending them into different positions as
the camera approaches.


Ambient Occlusion
-----------------

Basic ambient light assumes that every point on a surface is equally
affected by the light. This is simple, but unrealistic, as the light
from the background environment does not penetrate fully into crevasses.
Ambient Occlusion techniques aim to fix this.


### Ambient Occlusion Maps

These are a single channel of textures that are prebaked by the modeling
software. They...
* are fast,
* take up memory,
* do not react dynamically to changes in the environment.


### Screen Space Ambient Occlusion (SSAO)

Papers:
* ["Finding Next Gen - CryEngine 2", Mittring, 2007](https://web.archive.org/web/20170811191334id_/http://developer.amd.com/wordpress/media/2012/10/Chapter8-Mittring-Finding_NextGen_CryEngine2.pdf) chapter 8.5.4.3
* ["Hardware Accelerated Ambient Occlusion Techniques on GPUs"](http://www.okanarikan.com/assets/Papers/SSAO/paper.pdf)


### Horizon Based Ambient Occlusion (HBAO)

Papers:
* ["Image-Space Horizon-Based Ambient Occlusion", Bavoil, Sainz, Dimitrov, 2008](https://www.cse.chalmers.se/edu/year/2017/course/TDA361/Advanced%20Computer%20Graphics/Image-Space%20Horizon-Based%20Ambient%20Occlusion.pdf)


### Ambient Occlusion Volumes

Papers:
* ["Ambient Occlusion Volumes", McGuire, 2010](https://research.nvidia.com/sites/default/files/pubs/2010-06_Ambient-Occlusion-Volumes/McGuire10AOV.pdf)


### Scalable Ambient Occlusion (SAO, a.k.a. HBAO+)

Papers:
* ["Scalable Ambient Obscurance", McGuire, Mara, Luebke, 2012](https://research.nvidia.com/sites/default/files/pubs/2012-06_Scalable-Ambient-Obscurance/McGuire12SAO.pdf)


### Ground Truth Ambient Occlusion (GTAO)

Papers:
* ["Practical Real-Time Strategies for Accurate Indirect Occlusion", Jimenez, Wu, Pesce, Jarabo, 2016](https://www.activision.com/cdn/research/Practical_Real_Time_Strategies_for_Accurate_Indirect_Occlusion_NEW%20VERSION_COLOR.pdf)


### Visibility Bitmask Ambient Occlusion (VBAO)

Papers:
* ["Screen Space Indirect Lighting with Visibility Bitmask", Therrien, Levesque, Gilet, 2023](arxiv.org/pdf/2301.11376)


### Voxel-Accelerated Ambient Occlusion (VXAO)

FIXME


### Distance Fields Ambient Occlusion (DFAO)

FIXME


### Neural Network Ambient Occlusion (NNAO)

* ["Neural Network Ambient Occlusion", Holden, Saito, Komura, 2016](https://theorangeduck.com/media/uploads/other_stuff/nnao.pdf)
* [According to an author](https://theorangeduck.com/page/neural-network-ambient-occlusion),
  it can be improved upon by using the spiral-based sampling from SAO.


### Other links

* [GDC 2016 presentation on HBAO+, HBAO Ultra, and VXGI/VXAO](https://developer.download.nvidia.com/gameworks/events/GDC2016/atatarinov_alpanteleev_advanced_ao.pdf)


Shadow Volumes
--------------

FIXME: Meshes are extruded away from the shadow caster?
