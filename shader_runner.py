import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
import time

# Initialize Pygame and OpenGL
pygame.init()
display = (1920, 1080)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Vertex shader (minimal)
VERTEX_SHADER = """
#version 300 es
in vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

# Read fragment shader from file
with open('fragment_shader.glsl', 'r') as file:
    FRAGMENT_SHADER = file.read()

# Compile shaders
vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

# Create a fullscreen quad
vertices = np.array([-1.0, -1.0,
                     1.0, -1.0,
                    -1.0,  1.0,
                     1.0,  1.0], dtype=np.float32)

# Create VBO and upload data
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Set up vertex attributes
position_location = glGetAttribLocation(shader_program, 'position')
glEnableVertexAttribArray(position_location)
glVertexAttribPointer(position_location, 2, GL_FLOAT, GL_FALSE, 0, None)

# Get uniform locations
time_location = glGetUniformLocation(shader_program, 'u_time')
resolution_location = glGetUniformLocation(shader_program, 'u_resolution')

# Main loop
start_time = time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader_program)

    # Update uniforms
    current_time = time.time() - start_time
    glUniform1f(time_location, current_time)
    glUniform2f(resolution_location, display[0], display[1])

    # Draw fullscreen quad
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    pygame.display.flip()
    pygame.time.wait(10)
