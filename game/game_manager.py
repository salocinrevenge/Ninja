from jogador import Jogador
from enemy import Enemy
from pyray import Vector3
from camera import Camera
from controler import Controler
from game_chunk import Game_Chunk
from assets_loader import Assets_Loader
from block import Block
import random
import math
import pyray as rl
from utils import load_sky, draw_skybox

class Game_Manager():
    def __init__(self, motor):
        self.motor = motor
        self.assets_loader = Assets_Loader(self)
        self.jogador = Jogador(self)
        self.max_height = 16
        self.max_height = 256
        self.render_distance_skybox = 10000.
        try:
            rl.rl_set_clip_planes(0.1, self.render_distance_skybox)
        except:
            self.render_distance_skybox = 1000.
        self.create_map()
        self.sky_tex, self.sky_src = load_sky()
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
        rl.clear_background(rl.Color(120, 255, 255, 255))
        rl.draw_rectangle_gradient_v(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.Color(255, 255, 255, 0), rl.Color(255, 255, 255, 255))

        rl.begin_mode_3d(self.camera.camera)
        # self.draw_grid(20, 1.0)
        draw_skybox(self.camera.camera.position, self.sky_tex, self.sky_src, self.render_distance_skybox)
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
            self.loaded_chunks[new_coord] = Game_Chunk(self, new_coord.x, new_coord.z, max_height=self.max_height)
        self.center_chunks.append(self.loaded_chunks[new_coord])
        self.load_adjacent_chunks(new_coord)

    def load_adjacent_chunks(self, center_coord):
        directions = [(-16, 0), (16, 0), (0, -16), (0, 16),
                      (-16, -16), (-16, 16), (16, -16), (16, 16)]
        for dir in directions:
            neighbor_coord = (center_coord[0] + dir[0], center_coord[1] + dir[1])
            if neighbor_coord not in self.loaded_chunks:
                self.loaded_chunks[neighbor_coord] = Game_Chunk(self, neighbor_coord[0], neighbor_coord[1], max_height=self.max_height)

    def update(self, dt):
        self.input()
        for center in self.center_chunks:
            offsets = [(0, 0), (-16, 0), (16, 0), (0, -16), (0, 16),
                (-16, -16), (-16, 16), (16, -16), (16, 16)]
            for dx, dz in offsets:
                chunk = self.loaded_chunks.get((center.x + dx, center.z + dz))
                if chunk:
                    chunk.update(dt)
        alive_entities = []
        for entity in self.entities:
            entity.update(dt)
            if entity.alive:
                alive_entities.append(entity)
        self.entities = alive_entities
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
            if event == "F11_DOWN":
                self.motor.fullscreen_toggle()
                    

    def create_chunk(self,x,z):
        self.loaded_chunks.append(Game_Chunk(x,z,max_height=self.max_height))

    def unload_chunk(self,x,z):
        pass


    def create_map(self):
        self.center_chunks = []
        self.loaded_chunks = dict()

        self.loaded_chunks[self.jogador.chunck_coord] = Game_Chunk(self, *self.jogador.chunck_coord, max_height=self.max_height)
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

    def check_collision_with_blocks(self, x, y, z, dims=None, debug=False):
        chunk_coord = (int(math.floor(x / 16)) * 16, int(math.floor(z / 16)) * 16)
        chunk = self.loaded_chunks.get(chunk_coord)
        
        if chunk is None:
            return False
            
        if dims is None:
            # Checagem de um ponto específico (usado pelo raycast da câmera)
            block_id = chunk.get_block_global(int(math.floor(x)), int(math.floor(y)), int(math.floor(z)))
            return block_id > 0

        # Checagem de área (AABB) nos 8 vértices do jogador
        for dx in [-(dims.x/2), dims.x/2]:
            for dy in [0, dims.y/2, dims.y]:
                for dz in [-(dims.z/2), dims.z/2]:
                    check_x = int(math.floor(x + dx))
                    check_y = int(math.floor(y + dy))
                    check_z = int(math.floor(z + dz))
                    
                    block_id = chunk.get_block_global(check_x, check_y, check_z)
                    if block_id > 0:
                        return True
                        
        return False

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def dispose(self):
        self.assets_loader.clear_all()

    def add_spell(self, spell):
        self.entities.append(spell)

    def add_block(self, x, y, z, block_name):
        chunk_coord = (int(math.floor(x / 16)) * 16, int(math.floor(z / 16)) * 16)
        chunk = self.loaded_chunks.get(chunk_coord)
        if chunk:
            local_x = int(x - chunk.x)
            local_y = int(y)
            local_z = int(z - chunk.z)
            block = Block(self, self.assets_loader, block_name, Vector3(x, y, z))
            chunk.place_block(local_x, local_y, local_z, block)


