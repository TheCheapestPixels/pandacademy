#version 430

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 vertex;
in vec2 texcoord;
out vec2 uv;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  uv = texcoord;
}
