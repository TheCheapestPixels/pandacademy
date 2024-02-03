#version 430
#pragma include "cellular2D.glsl"

layout (local_size_x = 16, local_size_y = 16) in;

uniform float time;
layout(rgba32f) uniform writeonly image2D tex;

void main() {
  ivec2 texCoords = ivec2(gl_GlobalInvocationID.xy);
  ivec2 texSize = imageSize(tex);
  vec2 uv = vec2(texCoords) / vec2(texSize - 1);

  imageStore(tex, texCoords, vec4(0.5 + 0.5 * cellular(uv * 4.0).x));
}
