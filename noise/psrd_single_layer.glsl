#version 430
#define PI 3.1415926535897932384626433832795
#pragma include "psrdnoise2.glsl"

layout (local_size_x = 16, local_size_y = 16) in;

uniform float time;
layout(rgba32f) uniform writeonly image2D tex;

void main() {
  ivec2 texCoords = ivec2(gl_GlobalInvocationID.xy);
  ivec2 texSize = imageSize(tex);
  /* Size of the grid that we sample. */
  vec2 size = vec2(2.0, 2.0);
  vec2 uv = vec2(texCoords) / vec2(texSize - 1);
  /* The number in simplex grid tiles before the pattern wraps around,
     so that it tiles. Set this to 0 or negative for the pattern to
     not repeat. Note: `period.y` has to be an even number, as the
     lines along the x axis have their points alternatingly at the
     edges and the middle of the tile. */
  vec2 period = vec2(size);
  /* Gradient of the noise.
     If the gradient remains unused, the shader will be faster, as a
     bunch of code will be removed during compilation. */
  vec2 gradient;
  /* An alpha of 2*pi is a full rotation, so the animation here will
     repeat every second. */
  float speed = 2.0 * PI;

  /* Noise values are between -1 and 1, so we will need to scale them to
     the 0 to 1 range. */
  float value = 0.5 + 0.5 * psrdnoise(uv * size, period, time * speed, gradient);
  imageStore(tex, texCoords, vec4(value));
}
