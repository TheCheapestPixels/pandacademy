/* An experiment with layering psrd noise. The result is a pattern that
   loses a lot of the "bees dancing around each other" look of a single-
   layer psrdnoise, but which is not efficient in providing fine
   details, as it is making the layers linearly larger, not
   exponentially.
*/

#version 430
#define PI 3.1415926535897932384626433832795
#pragma include "psrdnoise2.glsl"

layout (local_size_x = 16, local_size_y = 16) in;

uniform float time;
layout(rgba32f) uniform writeonly image2D tex;

void main() {
  ivec2 texCoords = ivec2(gl_GlobalInvocationID.xy);
  ivec2 texSize = imageSize(tex);
  float size = 1.0;
  vec2 uv = vec2(texCoords) / vec2(texSize - 1);
  vec2 period = vec2(size);
  vec2 gradient = vec2(0.0);
  float speed = 1.0;

  float value = 0.5;
  value += 0.25   * psrdnoise((uv + vec2(0.0, 0.0   )) * size,        period,       time * speed,        gradient);
  value += 0.125  * psrdnoise((uv + vec2(0.0, 0.5   )) * size *  2.0, period * 2.0, time * speed *  2.0, gradient);
  value += 0.0625 * psrdnoise((uv + vec2(0.0, 0.1666)) * size *  3.0, period * 3.0, time * speed *  3.0, gradient);
  value += 0.03125 * psrdnoise((uv + vec2(0.0, 0.125)) * size *  4.0, period * 4.0, time * speed *  4.0, gradient);
  imageStore(tex, texCoords, vec4(value));
}
