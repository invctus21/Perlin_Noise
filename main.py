from ursina import *
from terrain_gen import generate_terrain

app = Ursina()

size = 20
terrain = generate_terrain(size=size)

for x in range(size):
    for z in range(size):
        height = terrain[x][z] * 3

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
            position=(x, height, z)
        )

# camera
camera.position = (size//2, 15, -size)
camera.rotation_x = 30

# lighting
DirectionalLight(y=2, z=3, shadows=True)
AmbientLight(color=color.rgba(100,100,100,0.5))

app.run()