from ursina import *
from perlin import perlin_octaves

app = Ursina()

chunk_size = 20

def generate_height(x, z):
    return perlin_octaves(x/20, z/20) * 3

def generate_terrain():
    for x in range(chunk_size):
        for z in range(chunk_size):
            height = generate_height(x, z)

            if height < 0.8:
                col = color.blue
            elif height < 1.2:
                col = color.yellow
            elif height < 2:
                col = color.green
            else:
                col = color.gray

            Entity(
                model='cube',
                color=col,
                position=(x, height, z),
            )

generate_terrain()

camera.position = (10, 30, -10)
camera.look_at(Vec3(10, 0, 10))

DirectionalLight(y=2, z=3, shadows=True)
AmbientLight(color=color.rgba(100, 100, 100, 0.5))

app.run()