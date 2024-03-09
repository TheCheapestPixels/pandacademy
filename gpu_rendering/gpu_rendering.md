Rendering and Shaders
---------------------

* [Minimal shader example](shaders/minimal/shader.py) demonstrates
  vertex and fragment shader. That is sufficient to explain the default
  shading pipeline, and show off first tricks.
* [All-stages example](shaders/all_stages/shader.py)
  * all five rendering shaders in action
  * hardware instancing.
* [Minimal compute shader](shaders/compute/main_basic_compute.py)
  * Writing textures
  * Texture-to-texture transformation
  * Extracting texture data from the GPU back to the `Texture` object.
* [Conway's Game of Life](shaders/compute/main_game_of_life.py)
  * Memory barrier
  * How to screw up:
    * Write back into the input texture. Race condition between
      workgroups result.
    * Don't load the Moore neighborhood. Performance evaporates.
