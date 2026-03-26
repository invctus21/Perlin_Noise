import numpy as np
from perlin import perlin_octaves

def generate_terrain(size=50, scale=20.0):
    terrain = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            terrain[i][j] = perlin_octaves(i/scale, j/scale)

    # normalize
    eps = 1e-9
    terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min() + eps)

    return terrain