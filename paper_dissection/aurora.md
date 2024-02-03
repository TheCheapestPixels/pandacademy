Simulating the Aurora Borealis
------------------------------

[Paper](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=f3bfb057bb50e020b7a14eb42cf97b562e169635)

* Summarizes auroral science
* Electrons from solar winds are caught by Earth's magnetic fields.
  * Macroscopically, they travel straight downwards, but microscopically they spin around the straight line.
  * On their way down, they collide with atoms and molecules, depositing energy, and getting deflected laterally.
  * Deposited energy gets reemitted as photons after a delay. The most important contributors are:
    * Red: Atomic oxygen, 630.0nm, ~110s, upper parts
    * Green: Atomic oxygen, 557.7nm, <0.7s, ~100km
    * Blue: Ionized nitrogen, 427.8nm, <0.001s, lower border
    An atom's movement during long reemission times may smear out the aurora. Atom-atom collisions remove the ability to re-emit (quenching).
* Electrons fall in sheets that are subject to curtain-like bending and folding.
  * Spirals: ~50km apart
  * Folds: ~ 20km apart, exist for more than a second
  * Curls: ~2-10km apart, 0.25-0.75s, cause rays of below 1km diameter
* TODO


Interactive Volume Rendering Aurora on the GPU
----------------------------------------------

[Paper](https://otik.uk.zcu.cz/bitstream/11025/1242/1/Lawlor.pdf)

* Very light on actual math, but references other papers for that purpose.
* Uses a geometry-free raytracing approach.
* The Lazarev charged particle energy deposition model is applied to the MSIS-E-90 atmosphere to create a lookup table.
  * LUT(input energy, atmospheric altitude) = relative deposited energy
* 2D splines to sketch out the footprint of an auroral storm on the planet.
* Splines get mapped to `curtain footprint`, a large 2D texture.
* From the `curtain footprint`, a lower-resolution `distance map` is created using jump flooding.
  * "Jump flooding in GPU with applications to Voronoi diagram and distance transform": https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=a797809529937a41abf7133e90914178a64b0897
* The raytracer uses the distance map to jump over empty space, but sample bands in detail.
  * Being too precise here can lead to performance losses due to the shader experiencing branch divergence.
* A periodic, thin, long strip of texture is tiled along the splines to create width.
* Fluid dynamics (2D Stam-type fluid advection simulator) on the strip create turbulence over the aurora's lifetime.
  * "Stable Fluids": https://cg.informatik.uni-freiburg.de/intern/seminar/gridFluids_StableFluids.pdf
    "We use a multigrid divergence correction approach for the Poisson step, which is both asymptotically faster than an FFT or conjugate gradient approach, and makes the simulator amenable to a graphics hardware implementation."
* The turbulent strip is used as the electron flux for the LUT.
* Map the aurora's emission peaks to CIE XYZ to sRGB, according to "Simulating the Aurora Borealis".
