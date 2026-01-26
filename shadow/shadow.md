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
* Hybrid Frustum-Traced Shadows (HFTS)
  * ["HFTS: Hybrid Frustum-Traced Shadows in “The Division”", Story, Wyman, 2016](https://cwyman.org/abstracts/sig2016_hfts.pdf)

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

Explanatory video: [Once Upon a Pixel: How Crysis Changed Real-Time Lighting Forever](https://www.youtube.com/watch?v=xq5hD4RGcYw)


### Horizon Based Ambient Occlusion (HBAO)

Papers:
* ["Image-Space Horizon-Based Ambient Occlusion", Bavoil, Sainz, Dimitrov, 2008](https://www.cse.chalmers.se/edu/year/2017/course/TDA361/Advanced%20Computer%20Graphics/Image-Space%20Horizon-Based%20Ambient%20Occlusion.pdf)


### Ambient Occlusion Volumes

Papers:
* ["Ambient Occlusion Volumes", McGuire, 2010](https://research.nvidia.com/sites/default/files/pubs/2010-06_Ambient-Occlusion-Volumes/McGuire10AOV.pdf)


### Scalable Ambient Occlusion (SAO, a.k.a. HBAO+ in nvidia parlance)

Papers:
* ["Scalable Ambient Obscurance", McGuire, Mara, Luebke, 2012](https://research.nvidia.com/sites/default/files/pubs/2012-06_Scalable-Ambient-Obscurance/McGuire12SAO.pdf)


### Ground Truth Ambient Occlusion (GTAO)

Papers:
* ["Practical Real-Time Strategies for Accurate Indirect Occlusion", Jimenez, Wu, Pesce, Jarabo, 2016](https://www.activision.com/cdn/research/Practical_Real_Time_Strategies_for_Accurate_Indirect_Occlusion_NEW%20VERSION_COLOR.pdf)


### Visibility Bitmask Ambient Occlusion (VBAO)

Papers:
* ["Screen Space Indirect Lighting with Visibility Bitmask", Therrien, Levesque, Gilet, 2023](arxiv.org/pdf/2301.11376)


### Voxel Ambient Occlusion (VXAO)

Uses world space occlusion tests.


### Distance Fields Ambient Occlusion (DFAO)

FIXME


### Neural Network Methods

* Neural Network Ambient Occlusion (NNAO)
  * ["Neural Network Ambient Occlusion", Holden, Saito, Komura, 2016](https://theorangeduck.com/media/uploads/other_stuff/nnao.pdf)
  * [According to an author](https://theorangeduck.com/page/neural-network-ambient-occlusion),
    it can be improved upon by using the spiral-based sampling from SAO.
* DeepAO
  * ["DeepAO: Efficient Screen Space Ambient Occlusion Generation via Deep Network", Dongjiu Zhang, Chuhua Xian, Guoliang Luo, Yunhui Xiong, Chu Han, 2020](https://github.com/chuhuaxian/DeepAO)


### Other techniques and variations

* [GDC 2016 presentation on HBAO+, HBAO Ultra, and VXGI/VXAO](https://developer.download.nvidia.com/gameworks/events/GDC2016/atatarinov_alpanteleev_advanced_ao.pdf)
* ["Stereo-consistent screen-space ambient occlusion", Shi, Billeter, Eisemann](https://pure.tudelft.nl/ws/portalfiles/portal/121484149/3522614.pdf): Dealing with real-time AO that needs to be consistent in two images.
* Alchemy AO: ["The Alchemy Screen-Space Ambient Obscurance Algorithm", McGuire, Osman, Bukowski, Hennessy, ????](https://casual-effects.com/research/McGuire2011AlchemyAO/VV11AlchemyAO.pdf)
* ["Screen-Space Ambient Occlusion Using A-buffer Techniques", Bauer, Knuth, Kuijper, Bender, ????](https://animation.rwth-aachen.de/media/papers/2013-CADGraphics-MultilayerAO.pdf)
* ["Separable Approximation of Ambient Occlusion", Huang, Boubekeur, Ritschel, Holländer, Eisemann, 2011](https://perso.telecom-paristech.fr/boubek/papers/SAO/SAO.pdf)
* Listed on Wikipedia
  * Screen space directional occlusion (SSDO)
  * Ray-traced ambient occlusion (RTAO)
    * https://github.com/boksajak/RTAO
  * High Definition Ambient Occlusion (HDAO)
  * Angle Based Ambient Occlusion (ABAO)
  * Pre Baked Ambient Occlusion (PBAO)
* Listed in ["A review of real-time global illumination rendering methods without preprocessing" (translated)](https://www.jcad.cn/en/article/pdf/preview/10.3724/SP.J.1089.2024-00683.pdf)
  * RSM (2005): [Reflective Shadow Maps](http://www.klayge.org/material/3_12/GI/rsm.pdf)
  * SSAO (2007): The Mittring publication
  * ISM (2008): [Imperfect Shadow Maps for Efficient Computation of Indirect Illumination](https://www.vclab.kaist.ac.kr/siggraphasia2008/ISM_SIGAsia08s.pdf)
  * SSDO (2009): Screen space directional occlusion, [Approximating Dynamic Global Illumination in Image Space](https://phaazon.net/media/uploads/SSDO.pdf)
  * LPV (2010): [Cascaded Light Propagation Volumes for Real-Time Indirect Illumination](https://cg.ivd.kit.edu/publications/p2010/CLPVFRII_Kaplanyan_2010/CLPVFRII_Kaplanyan_2010.pdf)
  * HBAO (2011)
  * VXGI (2011)
  * SSR (2014): No clue...
  * SVGF (2017) [Spatiotemporal Variance-Guided Filtering: Real-Time
Reconstruction for Path-Traced Global Illumination](https://cg.ivd.kit.edu/publications/2017/svgf/svgf_preprint.pdf)
  * DLSS (2018): Deep Learning Supersampling. Why is this here?
  * DDGI (2019): [Dynamic Diffuse Global Illumination with raytraced irradiance fields](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9900-irradiance-fields-rtx-diffuse-global-illumination-for-local-and-cloud-graphics.pdf)
    * Improved: https://cescg.org/wp-content/uploads/2022/04/Rohacek-Improving-Probes-in-Dynamic-Diffuse-Global-Illumination.pdf
  * ReSTIR DI (2020): Reservoir-based Spatio-Temporal Importance Resampling, [Spatiotemporal reservoir resampling for real-time ray tracing
with dynamic direct lighting](https://research.nvidia.com/sites/default/files/pubs/2020-07_Spatiotemporal-reservoir-resampling/ReSTIR.pdf)
  * NRC (2021) neural radiance caching, [Real-time Neural Radiance Caching for Path Tracing](https://d1qx31qr3h6wln.cloudfront.net/publications/mueller21realtime.pdf)
  * ReSTIR DI (2021) See above, [ReSTIR GI: Path Resampling for Real-Time Path Tracing](https://d1qx31qr3h6wln.cloudfront.net/publications/ReSTIR%20GI.pdf)
  * Lumen (2022)
  * GI-1.0 (2023): [GI-1.0: A Fast and Scalable Two-level Radiance Caching Scheme for Real-time Global Illumination](https://arxiv.org/pdf/2310.19855)
  * ExtraSS (2023): [ExtraSS: A Framework for Joint Spatial Super Sampling and Frame Extrapolation](ExtraSS: A Framework for Joint Spatial Super Sampling and Frame Extrapolation)
* A trick to improve SSAO sampling
  * ["How I Improved My Game Engine's SSAO With A Simple Trick"](https://www.youtube.com/watch?v=vJU1PgGdH3k),
    explanation in comments, reproduced with modification here.
  * Get the worldspace coord of the current fragment.
  * Loop over the array of poisson disk coordinates.
    * sample pos = fragment position + offset
    * Transform to world space coordinate
    * Test
      * if the sample is in the fragment's normal-based hemisphere.
      * if the sample is non-occluded on the depth map.
  * The ratio of positively testing samples is the occlusion.


Shadow Volumes
--------------

FIXME: Meshes are extruded away from the shadow caster?
