import math
import numpy as np
import matplotlib.pyplot as plt

SEED = 1013

# Gradient (deterministic)

def random_gradient(ix, iy):

    n = ix * 1836311903 ^ iy * 2971215073 ^ SEED
    n = (n << 13) ^ n
    rand = (n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff

    angle = (rand / 0x7fffffff) * 2 * math.pi
    return math.cos(angle), math.sin(angle)

# Dot product

def dot(g, dx, dy):
    return g[0] * dx + g[1] * dy

# Fade function

def fade(t):
    return 6*t**5 - 15*t**4 + 10*t**3

# Linear interpolation

def lerp(a, b, t):
    return a + t * (b - a)

# Perlin Noise (2D)

def perlin(x, y):
    # grid cell coordinates
    x0 = int(math.floor(x))
    y0 = int(math.floor(y))
    x1 = x0 + 1
    y1 = y0 + 1

    # local position
    dx = x - x0
    dy = y - y0

    # gradients at corners
    g00 = random_gradient(x0, y0)
    g10 = random_gradient(x1, y0)
    g01 = random_gradient(x0, y1)
    g11 = random_gradient(x1, y1)

    # dot products
    n00 = dot(g00, dx, dy)
    n10 = dot(g10, dx - 1, dy)
    n01 = dot(g01, dx, dy - 1)
    n11 = dot(g11, dx - 1, dy - 1)

    # fade curves
    u = fade(dx)
    v = fade(dy)

    # interpolation
    nx0 = lerp(n00, n10, u)
    nx1 = lerp(n01, n11, u)
    nxy = lerp(nx0, nx1, v)

    return nxy

# Octaves (multi-layer noise)

def perlin_octaves(x, y, octaves=5, persistence=0.5, lacunarity=2):
    value = 0
    amplitude = 1
    frequency = 1

    for _ in range(octaves):
        value += amplitude * perlin(x * frequency, y * frequency)
        amplitude *= persistence
        frequency *= lacunarity

    return value
