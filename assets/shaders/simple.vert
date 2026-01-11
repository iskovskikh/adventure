#version 330 core

layout (location = 0) in vec3 VertexPos;

out vec3 Color;

void main()
{
    gl_Position = vec4(VertexPos.xyz, 1.0);
    Color = vec3(1.0, 0.5, 0.2);
}