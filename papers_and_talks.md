Papers and Talks
================

A collection of videos, academic papers, and other media.


Artificial Intelligence
-----------------------

* Introductory overview on game theory: https://www.theorie.physik.uni-muenchen.de/lsfrey/teaching/archiv/sose_06/softmatter/talks/Heiko_Hotz-Spieltheorie-Handout.pdf
* The "Game AI Pro", collecting lots of various articles: http://www.gameaipro.com/
* [Artificial Intelligence: Foundations of Computational Agents](https://artint.info/3e//html/ArtInt3e.html)


### Navigation

* Navmesh-less navigation in Hyper Scape using neural networks: https://www.youtube.com/watch?v=DKdQFajLfzk https://arxiv.org/pdf/2011.04764.pdf


### Behavior trees

* Parallelism in Behavior Trees
  * "Improving the Parallel Execution of Behavior Trees": https://arxiv.org/pdf/1809.04898v1.pdf
    * Extends Behavior Trees by giving each node functions that report
      the node's current progress, and its use of resources.
    * Defines a `ParallelSync` node that routes ticks to the least
      progressed child tree.
    * Defines a `ParallelMutex` node that routes ticks to children with
      the highest priority (according to a policy that implements aging)
      as long as the necessary resources are available.
    * Both nodes, like the basic `Parallel`, fails if any child fails,
      succeeds when all children succeed, and otherwise remains active.
  * "Analysis and Exploitation of Synchronized Parallel Executions in
Behavior Trees": https://lornat75.github.io/papers/2019/colledanchise-iros.pdf
    * Builds on "Improving the Parallel Execution of Behavior Trees".
    * Defines `ParallelSyncAbsolute` that has a list of barrier values.
      If there are children with a progress below any given barrier, the
      children with progress equal to or above that barrier will no
      longer receive ticks.
    * Defines `ParallelSyncRelative` that ticks children so as to keep
      the slowest within a given range of the fastest.


### HTN: Hierarchical Task Networks

* "SHOP2: An HTN Planning System": https://arxiv.org/pdf/1106.4869.pdf
  * Foundational paper on HTN.
* "Automated Planning and Scheduling; Lecture 8: Hierarchical Planning": https://algo2.iti.kit.edu/balyo/plan/files/l08.pdf
  * Lecture slides on HTN basics
* "An Overview of Hierarchical Task Network Planning": https://www.researchgate.net/profile/Ilche-Georgievski/publication/261217494_An_Overview_of_Hierarchical_Task_Network_Planning/links/54f9a4760cf28d6deca5128a/An-Overview-of-Hierarchical-Task-Network-Planning.pdf
* "Hierarchical Task Network (HTN) Planning": https://pages.mtu.edu/~nilufer/classes/cs5811/2012-fall/lecture-slides/cs5811-ch11b-htn.pdf
  * Also lecture slides on HTN basics
* "Combining Domain-Independent Planning and HTN Planning: The Duet Planner": https://www.cs.umd.edu/~nau/papers/gerevini2008combining.pdf
  * Seems to combine GOAP and HTN.
* "On Hierarchical Task Networks": https://hal.science/hal-01692705/document
  * A definition of semantics for HTN
* "Learning Hierarchical Task Networks with Preferences from Unannotated Demonstrations": https://proceedings.mlr.press/v155/chen21d/chen21d.pdf
  * Learn tasks from examples, then optimize them.


### Search

* "Playing Your Cards Right: The Hierarchical Portfolio Search AI of Prismata": https://www.youtube.com/watch?v=sQSL9j7W7uA
  * A refinement for general tree search.
  * The problem: Searching through all possible combinations of
    fundamental actions leads to a prohibitively high branching factor.
  * Designers create portfolios of behaviors, which, given a state,
    execute actions. During search, portfolios provide valid
    combinations of behaviors, with which successor states are then
    generated. The branching factor thus is the number of behavior
    combinations.
  * Portfolios can be tailored to cause desired behavior patterns.
* "Three States and a Plan: The A.I. of F.E.A.R.": http://alumni.media.mit.edu/~jorkin/gdc2006_orkin_jeff_fear.pdf
  * A refinement of STRIPS planning.
  * Behaviors have preconditions that the state must fulfill for the
    behavior to be executable, and postconditions that will be fulfilled
    once the action is executed.
  * During search, behavior are concatenated into plans.


Procedural Generation
---------------------

### Noise

* "Landscape Automata for Search Based Procedural Content Generation": https://web.archive.org/web/20161002142355id_/http://eldar.mathstat.uoguelph.ca/dashlock/CIG2013/papers/paper_32.pdf


### Mesh and texture generation and transformation

* Manifold Dual Contouring: https://people.engr.tamu.edu/schaefer/research/dualsimp_tvcg.pdf
* "Procedural Generation of Rock Piles using Aperiodic Tiling": https://hal.science/hal-00463273/document
  Turn mesh volumes into rock piles with a technique similar to marching cubes.
* "Image Quilting for Texture Synthesis and Transfer": https://people.eecs.berkeley.edu/~efros/research/quilting/quilting.pdf
  Turns a small sample image of a kind-of-repetitive texture into a large one made up of copypasted bits.
  Can also do style transfer.


### Planets and Terrain

* How to create a geographical model of the planet. https://www.youtube.com/watch?v=sLqXFF8mlEU&ab_channel=SebastianLague
* Noise and terrain generation for beginners: https://youtu.be/CSa5O6knuwI
* "Fast Hydraulic Erosion Simulation and Visualization on GPU": https://xing-mei.github.io/files/erosion.pdf
* "Terrain Generation Using Procedural Models Based on Hydrology": https://hal.science/hal-01339224/file/siggraph2013.pdf
  Create river systems, then infer the terrain that created them.
* "Layered Data Representation for Visual Simulation of Terrain Erosion": http://data.exppad.com/public/papers/Layered_data_representation_for_Visual_Simulation_of_Terrain_Erosion.pdf
  Erosion that uses stacked layers of materials.
* "Procedural Generation of 3D Caves for Games on the GPU": https://lucris.lub.lu.se/ws/portalfiles/portal/6067634/5464988.pdf
  L-System-based
* "Ecologically Sound Procedural Generation of Natural Environments": https://pure.tudelft.nl/ws/files/36591423/36591255.pdf
* "Procedural Riverscapes": https://par.nsf.gov/servlets/purl/10167932
* "Procedural Generation of Mediterranean Environments": http://161.53.22.65/datoteka/821096.dcvis_18_3842.pdf
* "Generating Compelling Procedural 3D Environments and Landscapes": https://odr.chalmers.se/items/fbecc575-1358-4d5d-a35f-1b2af96e4763/full
* "A Review of Digital Terrain Modeling": https://hal.science/hal-02097510v1/document
* "A 3D visualisation environment modelling the evolution of north-west Europe since the Last Glacial Maximum": https://diglib.eg.org/bitstream/handle/10.2312/LocalChapterEvents.TPCG.TPCG07.229-235/229-235.pdf?sequence=1&isAllowed=y


### Cities and Buildings

* "Procedural Generation of Urban Landscape with Extended L-System for Virtual Worlds": https://core.ac.uk/download/pdf/223208563.pdf
* city generation: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.688.5908&rep=rep1&type=pdf & http://www.citygen.net/files/citygen_gdtw07.pdf
* About procgenning buildings and cities: https://www.youtube.com/watch?v=_1fvJ5sHh6A
* More on city generation: https://youtu.be/tQEQriDgKXY
* "Procedural Modeling of Cities": https://www.eecs.ucf.edu/~dcm/Teaching/COT4810-Spring2011/Literature/JamesGrisetti-ProceduralModelingofCities.pdf
  Takes maps (elevation, water, vegetation, population density, zoning, street style, etc.) and generates cities down to building facades.
* "Interactive Procedural Street Modeling": https://www2.cs.uh.edu/~chengu/Publications/streetModeling/street_sig08.pdf
* "The Dual Language of Geometry in Gothic Architecture: The Symbolic Message of Euclidian Geometry versus the Visual Symbolic Message of Euclidian Geometry versus the Visual Dialogue of Fractal Geometry Dialogue of Fractal Geometry": https://digital.kenyon.edu/cgi/viewcontent.cgi?article=1061&context=perejournal
  An analysis of geometry in Gothic architecture.
* "Procedural Design of Urban Open Spaces": https://papers.cumincad.org/data/works/att/ecaade2007_143.content.pdf


### Trees

* Real-Time Tree Rendering: https://www.academia.edu/download/66513149/978-3-540-25944-2_22.pdf
* Creation  and  Rendering  of  Realistic  Trees: https://courses.cs.duke.edu/fall02/cps124/resources/p119-weber.pdf
* Plastic Trees: Interactive Self-Adapting Botanical Tree Models: https://www.academia.edu/download/46163297/Plastic_trees_interactive_self-adapting_20160602-6738-5ro83z.pdf
* Rendering Leaves Using Hardware Tessellation: http://www.nik.no/2010/16-Skjermo.pdf
* Remodelling of Botanical Trees for Real-Time Simulation: http://diglib.eg.org/bitstream/handle/10.2312/LocalChapterEvents.TPCG.TPCG11.001-008/001-008.pdf


### Aurora Borealis / Australis

* "Simulating the Aurora Borealis": https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=f3bfb057bb50e020b7a14eb42cf97b562e169635
  See [Aurora paper dissections](paper_dissection/aurora.md)
* "Interactive Volume Rendering Aurora on the GPU": https://otik.uk.zcu.cz/bitstream/11025/1242/1/Lawlor.pdf
  See [Aurora paper dissections](paper_dissections/aurora.md)
* "Aurora Rendering with Sheet Modeling Technique": http://www.cs.rpi.edu/~cutler/classes/advancedgraphics/S09/final_projects/ng.pdf


### Other

#### Patterns

* "Revisiting Ad Quadratum and Ad Triangulum to Generate Hyperbolic Tessellations": https://archive.bridgesmathart.org/2022/bridges2022-387.pdf
  Generates tesselation for the ribbing on the domes of vaults.


#### Dendrites

* "Visual Simulation of Ice Crystal Growth": https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=8aa81aa45523c7fdc562ed191bb0b4514a6e850b
  Simulates the growth of ice on input textures.
* "Simulation of Dendritic Painting": https://diglib.eg.org/bitstream/handle/10.1111/cgf13955/v39i2pp597-606.pdf
* "Modeling Dendritic Shapes Using Path Planning": http://people.scs.carleton.ca/~mould/papers/den.pdf


#### Crystals

* "Interactive Modeling of Polyhedral Crystals": https://nakajima.cfbx.jp/IWAIT2021/papers/paper_26.pdf
  A bit thin, but a starting point for growths of crystals.


#### Periodic Tiles

* "Euclidean tilings by convex regular polygons": https://en.wikipedia.org/wiki/Euclidean_tilings_by_convex_regular_polygons
  Wikipedia is always a good entry point.
* "Infinite Tilings": https://schoengeometry.com/c-infintil.html


#### Wang Tiles

* "Wang Tiles": http://www.cr31.co.uk/stagecast/wang/array.html
  An explanation of different types of Wang Tiling, which uses a tileset to texture an image aperiodically.
* "Wang Tiles for Image and Texture Generation": https://kops.uni-konstanz.de/server/api/core/bitstreams/f74fb7e3-333f-43ac-91a7-9cbd26527d60/content
  Takes an input image, image quilts it, uses that as a basis for Wang tiles.


Graphics
--------

* Graphics
  * Sand rendering in journey: https://archive.org/details/GDC2013Edwards
  * Clustered Shading (supercedes Tiled Shading) as explained by inventor: https://www.youtube.com/watch?v=uEtI7JRBVXk
  * Dynamic Diffuse Global Illumination with Ray-Traced Irradiance Fields: https://www.jcgt.org/published/0008/02/01/paper-lowres.pdf
* Physics-based Rendering
  * Disney PBR paper: https://disney-animation.s3.amazonaws.com/library/s2012_pbs_disney_brdf_notes_v2.pdf
  * Epic PBR Siggraph presentation: https://cdn2.unrealengine.com/Resources/files/2013SiggraphPresentationsNotes-26915738.pdf
* Animation
  * AI learns martial arts from motion capture data: https://www.youtube.com/watch?v=t33jvL7ftd4
  * Advanced IK techniques: https://www.youtube.com/watch?v=KLjTU0yKS00
  * Relation between eye gaze and foot placement when walking over rough terrain: https://www.sciencedirect.com/science/article/pii/S0960982218303099 
  * Youtube channel about game animation: https://yewtu.be/channel/UCxO_ya-RmAXCXJCU54AxYFw
  * "5 ways to draw an outline": https://alexanderameye.github.io/notes/rendering-outlines/
* Decals
  * https://martindevans.me/game-development/2015/02/27/Drawing-Stuff-On-Other-Stuff-With-Deferred-Screenspace-Decals/
  * https://bartwronski.com/2015/03/12/fixing-screen-space-deferred-decals/
  * https://www.gamedevs.org/uploads/screenspace-decals-space-marine.pdf


Clouds and Water
----------------

* Jupyter notebooks accompanying a lecture on the Navier-Stokes equation, solving for the steady state: https://github.com/barbagroup/CFDPython
* Volumetric cloud research from Horizon Zero dawn: http://advances.realtimerendering.com/s2015/The%20Real-time%20Volumetric%20Cloudscapes%20of%20Horizon%20-%20Zero%20Dawn%20-%20ARTR.pdf
* Simulating cloud dynamics and rendering clouds: https://users.cg.tuwien.ac.at/bruckner/ss2004/seminar/A3b/Harris2003%20-%20Simulation%20of%20Cloud%20Dynamics%20on%20Graphics%20Hardware.pdf
* Simulation of Cloud Dynamics on Graphics Hardware: http://www.markmark.net/cloudsim/index.html
* Navier-Stokes equations to simulate clouds: https://www.youtube.com/watch?v=EULG6ZrBghk
* Interactive Simulation of Clouds Based on Fluid Dynamics: https://d-nb.info/1108555179/34
* Real-Time Eulerian Water Simulation Using a Restricted Tall Cell Grid: https://matthias-research.github.io/pages/publications/tallCells.pdf
* Water surface simulation: https://www.youtube.com/watch?v=Dqld965-Vv0


Networking
----------

* Lag compensation in Watch Dogs 2's peer-to-peer vehicles: https://www.youtube.com/watch?v=_8A2gzRrWLk


Game Design
-----------

* Game Balance Concepts course
  * Overview: https://www.youtube.com/watch?v=tR-9oXiytsk
  * Course: https://gamebalanceconcepts.wordpress.com/2010/07/07/level-1-intro-to-game-balance/
* MDA: A Formal Approach to Game Design and Game Research: http://courses.washington.edu/css385/2017.Spring/Readings/MDA.pdf
  * GMTK video explaining it: https://www.youtube.com/watch?v=iIOIT3dCy5w
  * Case study of applying MDA to the construction of a game to convey knowledge about traditional Indonesian weapons: https://eprints.umm.ac.id/73851/20/Husniah%20Fannani%20Kholimi%20Kristanto%20-%20Action%20Adventure%20Platformer%2C%20MDA%20Framework%20Playtesting%20Evaluation%20Gameflow%20Test%20and%20Traditional%20Indonesian%20Weapons.pdf
  * Another case study, this time a game to "Decrease Anxiety in Preschool-Aged Children With Acute Lymphoblastic Leukemia": https://games.jmir.org/2022/3/e37079/ 
* Building an Ontology of Boardgame Mechanics based on the BoardGameGeek Database and the MDA Framework: http://www.sbgames.org/sbgames2017/papers/ArtesDesignFull/175272.pdf
* Goldeneye N64 GDD: https://youtu.be/Z1Fx18cppZk?t=672
* Teaching God of War players all the mechanics: https://www.thegamer.com/respawn-design-director-god-of-war-enemies-combat-mechanics/ https://www.thegamer.com/respawn-design-director-god-of-war-boss-fight/
* Lessons learned on Duolingo: https://www.youtube.com/watch?v=i7_8TODHWRs 
* Metagame balance math: https://www.youtube.com/watch?v=miu3ldl-nY4
* Never Just One Problem design principle (God of War): https://www.youtube.com/watch?v=snFATnSgdNY 
* RPG design resources: https://www.reddit.com/r/RPGdesign/wiki/resources/


Storytelling
------------

* Open World stories in ink / inklewriter: https://www.youtube.com/watch?v=HZft_U4Fc-U
* Watch Dogs, generating plausible backstories based on presented characters: https://www.youtube.com/watch?v=SXn_c-HM0Vk
* Something about metric-ized characters (persons) in systematic games: https://www.youtube.com/watch?v=qX5-2D8SP5A
* Emergent interaction sequences in crowds in Watch Dogs 2: https://www.youtube.com/watch?v=LHEcpy4DjNc
* "Toward Automated Quest Generation in Text-Adventure Games" https://www.aclweb.org/anthology/2019.ccnlg-1.1.pdf
* "Non-Linear Quest Generation" https://www.aaai.org/ocs/index.php/FLAIRS/FLAIRS18/paper/viewFile/17606/16885
* "Let CONAN tell you a story: Procedural quest generation" https://www.aaai.org/ocs/index.php/FLAIRS/FLAIRS18/paper/viewFile/17606/16885
* "Constructive Generation Methods for Dungeons" https://www.wi.uni-muenster.de/sites/wi/files/users/mpreu_02/games-material/ba-vm-ss2015/marco_niemann_-_constructive_generation_methods_for_dungeons_-_thesis.pdf
* A formula for story structure: https://www.youtube.com/watch?v=8fXE-E1hjKk
* Narrative lego: https://www.youtube.com/watch?v=p40p0AVUH70
* What it takes to write stories for AAA games (Erik Wolpaw): https://youtu.be/RzkVD94yAmA


Petri Nets and Workflows
------------------------

Petri Nets are networks of Places, which can store markers, and
Transitions, which remove sets of markers from their input places, and
add markers to their output places. They are modeling systems similar to
how FSMs do it, and can algorithmically be transformed into FSMs, and
vice versa; They also can be tested algorithmically for possible
deadlocks and livelocks.

Workflows are a subset of Petri Nets, which find application in modeling
industrial processes.

* http://www.project-open.com/en/workflow-petri-nets
* http://mlwiki.org/index.php/Workflow_Nets
* http://www.workflowpatterns.com/patterns/


Things that don't fit into any category above
---------------------------------------------

* intuition vs intellect: https://youtu.be/m9OmHK2b6fE?t=4385
* Colour science and its applications: http://github.com/jeremyselan/cinematiccolor/raw/master/ves/Cinematic_Color_VES.pdf
* Designing Robotron2084: https://invidious.himiko.cloud/watch?v=zRNppH_SCTE (starts at 58:00)
* Very old panda3d scripts: https://project-archives.etc.cmu.edu/2003/spring/panda3d/docs/tutorial.shtml
* FUCK VIDEOGAMES: https://tinysubversions.com/fuckvideogames
* Pixar/Khan Academy course on how they make their movies: https://www.khanacademy.org/computing/pixar
* Who's afraid of the holodeck?: https://youtu.be/zQpaM0kEf70
* Stop Writing Classes: https://youtu.be/o9pEzgHorH0
* Cross-system executables in CPP: https://justine.lol/ape.html
* Futuristic typesetting https://typesetinthefuture.com/
* Lots of short videos, at least some of them gamedev-related: https://www.youtube.com/c/Garbaj/videos
* What went wrong with gaming (marketing)?: https://youtu.be/g16heGLKlTA?t=506
* Introduction on aerodynamics: https://github.com/barbagroup/AeroPython
* [How to build a BVH](https://jacco.ompf2.com/2022/04/13/how-to-build-a-bvh-part-1-basics/)