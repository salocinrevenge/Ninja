from jogador import Jogador
from enemy import Enemy
from pyray import Vector3
from camera import Camera
from block import Block
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
        self.draw_grid(20, 1.0)

        for lc in self.loaded_chunks:
            lc.render()
        for entity in self.entities:
            entity.render()
        for proj in self.projectiles:
            proj.render()

        rl.end_mode_3d()

        self.jogador.render_hud()

        rl.end_drawing()

    def update(self, dt):
        for lc in self.loaded_chunks:
            lc.update(dt)
        for entity in self.entities:
            entity.update(dt)
        self.camera.update(dt)
        new_projectiles = []
        for proj in self.projectiles:
            proj.update(dt)
            if proj.alive:
                new_projectiles.append(proj)
        self.projectiles = new_projectiles

    def create_chunk(self,x,z):
        self.loaded_chunks.append(Game_Chunk(x,z))

    def unload_chunk(self,x,z):
        pass


    def create_map(self):
        self.loaded_chunks = []
        
        self.entities = []
        self.projectiles = []

        self.gravity = 0.03
        self.air_resistance = 0.5

        for x in range(-16,32,16):
            for z in range(-16,32,16):
                self.loaded_chunks.append(Game_Chunk(self, x,z))

        # --- Inimigos ---
        self.enemies = []
        self.n_enemies = 3
        self.n_enemies = 0 
        for _ in range(self.n_enemies):
            enemy = Enemy(game = self,
                          pos = Vector3(random.uniform(-10, 10), 1, random.uniform(-10, 10)),
                          dir = random.uniform(0, math.tau),
                          speed = 0.05,
                          cooldown= random.uniform(2, 5),
                          player = self.jogador,
                          )
            self.enemies.append(enemy)
            self.entities.append(enemy)

    def check_collision_with_blocks(self, x, y, z, dims):
        # identifica qual chunk o jogador está
        chunk_x = int(math.floor(x / 16)) * 16
        chunk_z = int(math.floor(z / 16)) * 16
        for chunk in self.loaded_chunks:
            if chunk.x == chunk_x and chunk.z == chunk_z:
                local_x = int(x - chunk.x)
                local_y = int(y)
                local_z = int(z - chunk.z)
                block = chunk.get_block(local_x, local_y, local_z)
                if block is not None:
                    return True
                return False
        return False

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def dispose(self):
        self.assets_loader.clear_all()



