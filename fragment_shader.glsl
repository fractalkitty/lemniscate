#version 300 es
precision mediump float;

uniform float u_time;
uniform vec2 u_resolution;

out vec4 fragColor;

float lemniscate(vec2 p) {
    // Scale the coordinate system
    p *= 2.2;

    // Calculate the lemniscate formula: (x² + y²)² = 2a²(x² - y²)
    float a = 1.0;
    float left = (p.x * p.x + p.y * p.y) * (p.x * p.x + p.y * p.y);
    float right = 2.0 * a * a * (p.x * p.x - p.y * p.y)*cos(u_time);

    // Return distance field
    return abs(left - right);
}

void main() {
    // Center and normalize coordinates
