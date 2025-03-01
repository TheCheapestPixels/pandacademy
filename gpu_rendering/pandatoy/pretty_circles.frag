#version 430

uniform float dt;
uniform float time;
uniform vec2 aspect;
in vec2 uv;
out vec4 fragColor;

void main() {
  vec2 uv0 = (uv.xy * 2 - 1) * aspect;
  float dist = length(uv0);
  float intensity = sin(dist * 50 + time * 20) * 0.5 + 0.5;
  fragColor = vec4(vec3(intensity), 1);
}
