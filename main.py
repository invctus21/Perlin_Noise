from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from terrain_gen import generate_terrain

app = Ursina()

chunk_size = 10
render_distance = 1
chunks={}

last_chunk = None

def generate_chunk(cx,cz):
    entities=[]

    for x in range(chunk_size):
        for z in range(chunk_size):

            world_x = cx * chunk_size + x
            world_z = cz * chunk_size + z

            height = generate_height(world_x,world_z)

            if height < 0.8:
                col = color.blue
            elif height < 1.2:
                col = color.yellow
            elif height < 2:
                col = color.green
            else:
                col = color.gray

            cube = Entity(
                model='cube',
                color=col,
                position=(world_x, height, world_z),
                collider='box'
            )

            entities.append(cube)

        return entities

from perlin import perlin_octaves

def generate_height(x, z):
    return perlin_octaves(x/20, z/20) * 3

def update_chunks():
    px = int(player.x // chunk_size)
    pz = int(player.z // chunk_size)

    needed = set()

    for dx in range(-render_distance, render_distance+1):
        for dz in range(-render_distance, render_distance+1):
            needed.add((px+dx, pz+dz))

    # load chunks
    for chunk in needed:
        if chunk not in chunks:
            chunks[chunk] = generate_chunk(*chunk)

    # unload chunks
    for chunk in list(chunks.keys()):
        if chunk not in needed:
            for e in chunks[chunk]:
                destroy(e)
            del chunks[chunk]

player = FirstPersonController()
player.position = (0, 5, 0)

# lighting
DirectionalLight(y=2, z=3, shadows=True)
AmbientLight(color=color.rgba(100,100,100,0.5))

def update():
    global last_chunk
    px = int(player.x//chunk_size)
    pz = int(player.z//chunk_size)

    current_chunk = (px,pz)

    if current_chunk != last_chunk:
        update_chunks()
        last_chunk = current_chunk

app.run()