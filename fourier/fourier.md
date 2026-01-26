Fourier Transform
=================

### What are they?

Fourier transforms are the class of functions that
* take a signal as input, and output the spectrum of the signal,
* or do the reverse (spectrum to signal, inverse Fourier transform).

The signal may be of arbitrary dimensionality. Typically, we deal with
* one-dimensional real-valued signals, e.g. sound
* two-dimensional real-valued signals, e.g. images

Signals may be
* continuous: For any coordinate, there is a known value. These are
  rarely of use to us in game development, since incoming data isn't
  continuous.
* discrete, meaning data points sampled at a regular interval. This is
  the standard case.

The spectrum is the parameters of a set of sinusoidal waves that, when
summed up, yield the input signal. Sinusoidal waves are those functions
that look like a sine wave if you squint enough to make the axes
disappear; That means that they are sine (or cosine) waves with
* frequency
* phase
* amplitude


### What do we use them for?

Many effects can be realized easily and efficiently when they are seen
as operations on the frequencies of an input. The input is transformed
into its spectrum representation, the effect is applied, and the updated
spectrum is transformed back. For example:
* High- and low-pass filters: Setting frequency ranges to zero. This
  makes sound tinnier or muffled, while it sharpens or blurs fine
  details in images.
* Equalizer
* The Doppler effect and color shifting can be achieved by moving the
  spectrum's data point into lower/higher frequencies.
* Echo and bloom can be implemented as convolutions, meaning that the
  input's spectrum is multiplied with an impulse response.


Continuous Fourier Transform
----------------------------

We will not be diving deeply into continuous Fourier Transform, as it
isn't of much practical use for us. It is, however, helpful to build up
some intuitions about the process that will come in helpful when going
over the discrete Fourier Transform.

Let's make some assumptions:
* We have a continuous, real-valued signal (for example the electrical
  signal from a microphone, or the tides in a river); While Fourier
  transforms can work with complex-valued signals as well, real values
  offer a simpler case.
* The signal is periodic, repeating infinitely. If it isn't, for example
  because we are working on a small snippet of sound from a song, we can
  still pretend that the signal is one period.
* The signal is a sum of sinusoidal waves. It probably isn't, but we can
  still decompose it as if it was.

Next, a bit of geometric intuition. Let's say we draw the signal on a
thin strip of paper. Then we twist the paper around its lengthwise axis
a few times. Now we look down that axis, and now the signal is a
radius-modulated spiral. If we sum it up (take the integral), something
interesting happens: If there was a sinusoid in the signal that had a
frequeny equal to how often we twisted the strip of paper around, the
sum will be off the axis, while sinusoids of all other frequencies will
have sums close to zero.

This is a very approximate description, though.	If the twist is only
slightly off, the resulting signal is not completely gone, but falls off
quite quickly, even below the zero line, before oscillation around it
while becoming lower and lower in amplitude the farther we go from the
peak.

If we now start with an untwisted paper, and plot the point of sums
against the current twist, the resulting graph is the spectrum of the
input signal. It may be rather fuzzy compared to what we would expect
when we apply the algorithm to e.g. a pure sine signal, but if we apply
the algorithm in reverse, it will still reconstruct the original signal.


Discrete Fourier Transform (DFT)
--------------------------------

Instead of pondering abstract mathematical concepts, let's ponder a
pragmatic case; That we have a real-valued signal that was sampled at
some regular intervals, like a `.wav` file sampled at 44.1kHz, which we
will sample at whole-numbered frequencies.

That means that instead of a tape of paper, we have a bunch of discs on
a string, representing the points in time at which we sample the signal.
As we turn them to rebuild the tape's twist, something interesting
happens...


### Shannon-Nyquist sampling theorem

At a frequency of 1, we turn each disk 1/44100th of a rotation. At a
frequency of 44099, we turn it 44099/44100th, but this is also
equivalent to turning it -1/44100th. The spirals that we are creating
are the same, just mirrored. This trend continues; For every frequency f
(except for 0 and 22050, which are their own mirrors), there is a
frequency 44100-f that mirrors it, and thus we are effectively sampling
the lower frequency again, but with opposite phase. From that follows:

* To sample a signal's frequency, the number of sample points must be
  more than twice the frequency.
* Sampling at a frequency higher than that creates an aliased signal.

Therefore, we will only consider the frequencies 0 to 22050.


### Amplitude

Since our sampling discs at 0 an 22050 are their own mirrors, they exist
only on the real axis:
* The DC bin at frequency 0. No rotation.
* Nyquist frenquency: This frequency, half that of the sample size (here
  22050), is only present in even-numbered sample sizes. Its samples
  alternate between no and half a rotation.

FIXME: I don't fully understand the maths of this myself yet, but in all
other frequencies, we're basically summing up rotated unit vectors, so
the sum's distance from the origin is only half that of the signal that
went into it. For these special cases, that is not the case.


### Code

With some intuition in place, [let's now hit the metal](./dft.py).


Fast Fourier Transformation
---------------------------

A group of algorithms that use clever tricks to lower the effort to
calculate the DFT.

* Cooley-Tukey (DIT, Decimation In Time)
  * ["An Algorithm for the Machine Calculation of Complex Fourier Series"](https://www.ams.org/journals/mcom/1965-19-090/S0025-5718-1965-0178586-1/S0025-5718-1965-0178586-1.pdf)
* Stockham (DIF, Decimation In Frequency)
* FFTW: https://www.fftw.org/fftw-paper-ieee.pdf
  * C library
  * builds Cooley-Tukey-similar FFTs from fundamental codelets
  * Seems best-in-class on CPU, but also addresses SIMD architectures.
* History lesson
  * ["Gauss and the history of the fast Fourier transform"](https://www.researchgate.net/profile/Charles-Burrus/publication/226049108_Gauss_and_the_history_of_the_fast_Fourier_transform/links/0c960533d71185d882000000/Gauss-and-the-history-of-the-fast-Fourier-transform.pdf)
  * ["History of the Fast Fourier Transform with J.W. Cooley and John Tukey"](https://www.youtube.com/watch?v=SK2XpvwU038)
* More papers
  * ["Fast Fourier Transform", Franz Franchetti and Markus Püschel], (https://users.ece.cmu.edu/~franzf/papers/fft-enc11.pdf)
  * ["Fast Fourier Transform on CPU and GPU", Chia-Lun Tsai](https://ctsai.me/portfolio/fft/FFT-report.pdf)


Math
----

FIXME: This should be spun off into its own course.

### Sinusoidal wavs

We build a general sinusoidal wave in complex space:
```python
from math import e, sin, cos


x = 2
# Basic wave (Euler's formula)
e ** (x * 1j) == cos(x) + sin(x) * 1j
# With phase `p`
p = 1.0
e ** ((x + p) * 1j) == cos(x + p) + sin(x + p) * 1j
# With frequency `f`
f = 3.0
e ** ((x * f + p) * 1j) == cos(x * f + p) + sin(x * f + p) * 1j
# With amplitude `a`
a = 1.5
a * e ** ((x * f + p) * 1j) == a * cos(x * f + p) + a * sin(x * f + p) * 1j
```
The shift will pop up in the frequency 0.


### Matrix multiplication (mat-mat and mat-vec)
### Matrix transpose
### Matrix inversion


Sources
-------

* DFT: https://www.youtube.com/watch?v=yYEMxqreA10
