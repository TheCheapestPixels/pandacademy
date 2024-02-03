#version 430
#define PI 3.1415926535897932384626433832795
#pragma include "classicnoise2D.glsl"

layout (local_size_x = 16, local_size_y = 16) in;

uniform float time;
layout(rgba32f) uniform writeonly image2D tex;

void main() {
  ivec2 texCoords = ivec2(gl_GlobalInvocationID.xy);
  ivec2 texSize = imageSize(tex);
  vec2 uv = vec2(texCoords) / vec2(texSize - 1);

  // `cnoise(uv)` gives non-tiling Perlin noise,
  // `pnoise(uv, period)` the tiling one.
  imageStore(tex, texCoords, vec4(0.5 + 0.5 * pnoise(uv * 4.0, vec2(4.0))));
}
