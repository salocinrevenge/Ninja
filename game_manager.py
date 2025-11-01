from jogador import Jogador
from enemy import Enemy
from pyray import Vector3
from camera import Camera
from controler import Controler
from game_chunk import Game_Chunk
from assets_loader import Assets_Loader
import random
import math
import pyray as rl

class Game_Manager():
    def __init__(self, motor):
        self.motor = motor
        self.assets_loader = Assets_Loader(self)
        self.jogador = Jogador(self)
        self.create_map()
        self.camera = Camera(self, self.jogador)
        self.entities.append(self.jogador)
        self.controls = Controler()

    
    def draw_grid(self, size=20, spacing=1.0):
        for i in range(-size, size + 1):
            rl.draw_line_3d(Vector3(i * spacing, 0, -size * spacing),
                            Vector3(i * spacing, 0, size * spacing),
                            rl.GRAY)
            rl.draw_line_3d(Vector3(-size * spacing, 0, i * spacing),
                            Vector3(size * spacing, 0, i * spacing),
                            rl.GRAY)

    def render(self):

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(self.camera.camera)
        # self.draw_grid(20, 1.0)

        # Renderizar apenas o chunk central e seus 8 vizinhos
        for center in self.center_chunks:
            offsets = [(0, 0), (-16, 0), (16, 0), (0, -16), (0, 16),
                (-16, -16), (-16, 16), (16, -16), (16, 16)]
            for dx, dz in offsets:
                chunk = self.loaded_chunks.get((center.x + dx, center.z + dz))
                if chunk:
                    chunk.render()
        for entity in self.entities:
            entity.render()
        for proj in self.projectiles:
            proj.render()

        looked_block = self.camera.get_block_looked_at()
        if looked_block:
            bx, by, bz, face = looked_block
            rl.draw_cube(Vector3(bx + 0.5, by + 0.5, bz + 0.5), 1, 1, 1, rl.Color(255, 255, 255, 51))  # White with 20% opacity (51/255)

        rl.end_mode_3d()

        self.jogador.render_hud()

        rl.end_drawing()

    def update_chunk(self, old_coord, new_coord):
        if old_coord != (None, None):
            self.center_chunks.remove(self.loaded_chunks[old_coord])
        if new_coord not in self.loaded_chunks:
            self.loaded_chunks[new_coord] = Game_Chunk(self, new_coord.x, new_coord.z)
        self.center_chunks.append(self.loaded_chunks[new_coord])
        self.load_adjacent_chunks(new_coord)

    def load_adjacent_chunks(self, center_coord):
        directions = [(-16, 0), (16, 0), (0, -16), (0, 16),
                      (-16, -16), (-16, 16), (16, -16), (16, 16)]
        for dir in directions:
            neighbor_coord = (center_coord[0] + dir[0], center_coord[1] + dir[1])
            if neighbor_coord not in self.loaded_chunks:
                self.loaded_chunks[neighbor_coord] = Game_Chunk(self, neighbor_coord[0], neighbor_coord[1])

    def update(self, dt):
        self.input()
        for center in self.center_chunks:
            offsets = [(0, 0), (-16, 0), (16, 0), (0, -16), (0, 16),
                (-16, -16), (-16, 16), (16, -16), (16, 16)]
            for dx, dz in offsets:
                chunk = self.loaded_chunks.get((center.x + dx, center.z + dz))
                if chunk:
                    chunk.update(dt)
        for entity in self.entities:
            entity.update(dt)
        self.camera.update(dt)
        new_projectiles = []
        for proj in self.projectiles:
            proj.update(dt)
            if proj.alive:
                new_projectiles.append(proj)
        self.projectiles = new_projectiles

    def input(self):
        events = self.controls.get_controls()
        for event in events:
            self.jogador.input(event)

    def create_chunk(self,x,z):
        self.loaded_chunks.append(Game_Chunk(x,z))

    def unload_chunk(self,x,z):
        pass


    def create_map(self):
        self.center_chunks = []
        self.loaded_chunks = dict()

        self.loaded_chunks[self.jogador.chunck_coord] = Game_Chunk(self, *self.jogador.chunck_coord)
        self.update_chunk((None, None), self.jogador.chunck_coord)
        
        self.entities = []
        self.projectiles = []

        self.gravity = 0.02
        self.air_resistance = 0.5

        # for x in range(-16,32,16):
        #     for z in range(-16,32,16):
        #         self.loaded_chunks.append(Game_Chunk(self, x,z))

        # --- Inimigos ---
        self.enemies = []
        self.n_enemies = 3
        self.n_enemies = 0 
        for _ in range(self.n_enemies):
            enemy = Enemy(game = self,
                          pos = Vector3(random.uniform(-10, 10), 3, random.uniform(-10, 10)),
                          dir = random.uniform(0, math.tau),
                          speed = 0.05,
                          cooldown= random.uniform(2, 5),
                          player = self.jogador,
                          )
            self.enemies.append(enemy)
            self.entities.append(enemy)

    def check_collision_with_blocks(self, x, y, z, dims, debug = False):
        chunk = self.loaded_chunks.get((int(math.floor(x / 16)) * 16, int(math.floor(z / 16)) * 16))
        if dims == None:
            local_x = int(x - chunk.x)
            local_y = int(y)
            local_z = int(z - chunk.z)
            block = chunk.get_block(int(math.floor(local_x)), int(math.floor(local_y)), int(math.floor(local_z)))
            return block is not None
        # Check all 8 corners of the parallelepiped

        for dx in [-(dims.x/2), dims.x/2]:
            for dy in [0, dims.y]:
                for dz in [-(dims.z/2), dims.z/2]:
                    if debug:
                        print("Checking collision at:", local_x + dx, local_y + dy, local_z + dz)
                    check_x = (x + dx - chunk.x)
                    check_y = (y + dy)
                    check_z = (z + dz - chunk.z)
                    check_x = int(math.floor(check_x))
                    check_y = int(math.floor(check_y))
                    check_z = int(math.floor(check_z))
                    block = chunk.get_block(check_x, check_y, check_z)
                    if block is not None:
                        return True
        return False

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def dispose(self):
        self.assets_loader.clear_all()



