from math import e, pi, sin, cos
from cmath import phase


# TODO:
# * Signal reconstruction: Why does the Nyquist freq not scan properly?
# * So many FIXMEs in the comments...
# * 2D signal
# * dealing with small sampling windows (split-second windows detect
#   20Hz how?)


# I really hope that you know matrix multiplication already...
def mat_mul(mat, vec):
    prod = [
        sum(mval * vval for mval, vval in zip(row, vec))
        for row in mat
    ]
    return prod
def invert_mat(mat):
    n = len(mat)
    augmented = [
        row[:] + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(mat)
    ]
    for i in range(n):
        if augmented[i][i] == 0:
            for r in range(i + 1, n):
                if augmented[r][i] != 0:
                    augmented[i], augmented[r] = augmented[r], augmented[i]
                    break
            else:
                raise ValueError("Matrix is not invertible")
        pivot = augmented[i][i]
        for j in range(2 * n):
            augmented[i][j] /= pivot
        for r in range(n):
            if r != i:
                factor = augmented[r][i]
                for c in range(2 * n):
                    augmented[r][c] -= factor * augmented[i][c]

    inv_mat = [row[n:] for row in augmented]
    return inv_mat
    

# Let's do a DFT (Discrete Fourier Transformation)! And for that, let's
# pretend that we've got an assumed-to-be-periodic input signal, want to
# know how much of a certain frequency is contained in it. So we create
# a vector of the same length that contains a signal of that frequency;
# Now we have two vectors that we can compare by taking their dot
# product.
def sampling_vec(freq, n):
    return [sampling_point(freq, x/n) for x in range(n)]


# So what are the data points of those sampling signals?
# By using a complex-valued sinusoidal, we avoid having to deal with
# separate sine and cosine components.
def sampling_point(freq, x):
    return e ** -(x * freq * 2.0 * pi * 1j)


# Now we stack up sampling vectors into a matrix.
def sampling_mat(freqs):
    n = len(freqs)
    mat = [sampling_vec(freq, n) for freq in freqs]
    return mat


# All that we need now is a way to stop pretending, and create a signal
# that we can analyze.
def make_demo_signal(n, *params):
    signal = [
        sum(a * cos(x/n * 2*pi * f + p) for f, a, p in params)
        for x in range(n)
    ]
    return signal


# To summarize: We can now...
# * construct an input signal,
# * construct a sampling matrix,
# * multiply the two.
# So far, so good. So let's do te analysis process.
def analyze(mat, signal):
    spectrum = mat_mul(mat, signal)
    # And with that, were done! ... If only it were that easy, right?
    #
    # If you were to comment out the rest of this function (except for
    # the `return spectrum`, of course, you would see something
    # peculiar; For most signals, there is a second signal at a higher
    # frequency, "mirrored" at a frequency half the window length, and
    # if you look at the amplitudes, you see that both the actual signal
    # that we want and its mirror copy are both half of that which we
    # put into the input signal. So where did those come from?
    #
    # We create our sampling frequencies by twisting a unit vector
    # around the origin of the complex plane. Let's assume that our
    # window length is 8. At sample 0, all sampling points are at 1+0j;
    # So far, so good. At frame 1, for the frequency 1, the point is
    # turned 1/8th of the full circle. Simultaneously, for the frequency
    # 7, the turn is 7/8th, equivalent to a -1/8th turn. This makes the
    # two sampling points complex conjugates of each other. As the input
    # signal is real-valued, multiplying signal and sampling point
    # linearly scales up the vector, resulting in the same magnitude for
    # either sampling point. Adding those samples up for all frames then
    # still results in the same magnitude, just with the sign of the
    # complex part switched.
    #
    # Thus we can only sample frequencies lower than half the size of
    # our window; This is the Shannon-Nyquist theorem.
    #
    # So what do we do now? First, we just throw away the frequencies
    # that are too high not to be aliases. Except for the Nyquist
    # frequency, if it exists, because apparently we need it for
    # synthesis. FIXME: Wat
    window_length = len(signal)
    spectrum = spectrum[:(window_length+2)//2]
    # FIXME: But where does the factor for non-DC, non-Nyquist
    # frequencies come from exactly?
    # Secondly, we now double the amplitude of every signal that is
    # affected by there being a paired alias.
    def scale(window_length, frame, spectrum_peak):
        if frame == 0 or frame == window_length / 2 + 1:
            return spectrum_peak
        return spectrum_peak * 2.0
    spectrum = [
        scale(window_length, f, s)
        for f, s in enumerate(spectrum)
    ]
    # FIXME: Explain how this following factor comes about.
    # Okay, one last tweak. The spectrum still needs to be scaled by the
    # window size to make the amplitudes come out right.
    spectrum = [s / window_length for s in spectrum]
    # And with that, we are actually, finally done.
    return spectrum


def synthesize(mat, spectrum):
    # As we refined the spectrum that came out of the analysis matrix,
    # we have to go the reverse road to get a spectrum to pass through
    # the synthesis matrix.
    #
    # So, first, scale up by the window size.
    window_length = len(mat)
    spectrum = [s * window_length for s in spectrum]
    # Secondly, we undo the scaling for non-DC, non-Nyquist frequencies
    def scale(window_length, frame, spectrum_peak):
        if frame == 0 or frame == window_length / 2:
            return spectrum_peak
        return spectrum_peak / 2.0
    spectrum = [
        scale(window_length, f, s)
        for f, s in enumerate(spectrum)
    ]
    # Thirdly, we reconstruct the high-frequency components as the
    # convex conjugate of their lower-frequency pair; That means we flip
    # the sign on the complex component, and that's it. This way, the
    # reconstructed signal will come out real-valued.
    # FIXME: And if we skip it, will the real components still be right?
    def reconstruct(spectrum, window_length, idx):
        if idx < len(spectrum):
            return spectrum[idx]
        return spectrum[window_length - idx].conjugate()
    spectrum = [
        reconstruct(spectrum, window_length, idx)
        for idx in range(window_length)
    ]
    # Finally we can now synthesize the signal.
    #import pdb; pdb.set_trace()
    signal = mat_mul(mat, spectrum)
    return signal


# So let's construct a signal!
window_length = 8  # Let's not overwhelm the output.
# The sinusoidal waves.
signal_params = [  # (Frequency, amplitude, phase)
    #(0.0, 1.0, 0.0),
    (4.0, 1.0, pi),
    #(4.0, 0.5, 1.0),
]
# A signal may also contain a "DC offset", which puts the waves
# off-center. Imagine that the signal is voltage measurements from a
# microphone; The interesting stuff is in the AC signal that comes from
# the mic's membrane vibrating back and forth, but due to the technical
# construction, there may also be a DC voltage on the line. When
# analyzing such a signal, that offset will appear as the signal with
# frequency 0.
signal = make_demo_signal(
    window_length,
    *signal_params,
)


# Now comes the analysis. Note that frequencies are relative to the
# window length, meaning that the whole of its length is, for the
# purposes of the sinusoidal waves in it, its length is 2*pi.
freqs = range(window_length)
analysis_mat = sampling_mat(freqs)
spectrum = analyze(analysis_mat, signal)


# And back to a signal again!
synthesis_mat = invert_mat(analysis_mat)
new_signal = synthesize(synthesis_mat, spectrum)


# And now let us take a look at our data...
print(f"Samples in signal: {window_length}")
print()
print("Signal is the sum of:")
for f, a, p in signal_params:
    print(f"  Frequency {f}: Amplitude {a: 1.3f}, phase {p: 1.3f}")
print("Detected spectrum:")
for f, v in zip(freqs, spectrum):
    print(f"  Frequency {f:1.1f}: Amplitude {abs(v): 1.3f}, phase {phase(v): 1.3f}")
print()
print("frame   Input signal    Reconstructed    Difference    Synth phase")
for frame, (v_in, v_out) in enumerate(zip(signal, new_signal)):
    print(f"{frame:3d}      {v_in: 1.3f}            {v_out.real: 1.3f}          {(v_out-v_in).real: 1.3f}        {v_out.imag: 1.3f}")
print()
print("Product of analysis and synthesis matrix (should be the identity matrix):")
for syn_vec in synthesis_mat:
    identity = mat_mul(analysis_mat, syn_vec)
    print('   '.join(f"{v: 1.1f}" for v in identity))
