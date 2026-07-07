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
from chunk_generator import ChunkGenerator

class DummyCenter:
    def __init__(self, x, z):
        self.x, self.z = x, z

class Game_Manager():
    def __init__(self, motor):
        self.motor = motor
        self.assets_loader = Assets_Loader(self)
        self.jogador = Jogador(self)
        self.max_height = 256
        self.render_distance_skybox = 10000.
        try:
            rl.rl_set_clip_planes(0.1, self.render_distance_skybox)
        except:
            self.render_distance_skybox = 1000.
        
        # IMPORTANTE: Definir o raio ANTES de criar o mapa inicial
        self.render_distance_chunks = 4  # Ajuste para 16 quando quiser testar o limite máximo
        
        # Inicializa o Multiprocessing
        self.chunk_generator = ChunkGenerator(self.max_height)
        self.requested_chunks = set() # Chunks que já foram pedidos ao processador

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
        draw_skybox(self.camera.camera.position, self.sky_tex, self.sky_src, self.render_distance_skybox)
        
        r = self.render_distance_chunks
        for center in self.center_chunks:
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    chunk_x = center.x + (dx * 16)
                    chunk_z = center.z + (dz * 16)
                    
                    # RENDERIZA APENAS SE ESTIVER CARREGADO
                    chunk = self.loaded_chunks.get((chunk_x, chunk_z))
                    if chunk:
                        chunk.render()

        for entity in self.entities:
            entity.render()
        for proj in self.projectiles:
            proj.render()

        looked_block = self.camera.get_block_looked_at()
        if looked_block:
            bx, by, bz, face = looked_block
            rl.draw_cube(Vector3(bx + 0.5, by + 0.5, bz + 0.5), 1, 1, 1, rl.Color(255, 255, 255, 51))

        rl.end_mode_3d()
        self.jogador.render_hud()
        rl.end_drawing()

    def update_chunk(self, old_coord, new_coord):
        if old_coord != (None, None):
            # Cuidado ao remover: garanta que o chunk existe antes de tentar remover do center_chunks
            chunk = self.loaded_chunks.get(old_coord)
            if chunk in self.center_chunks:
                self.center_chunks.remove(chunk)
                
        # Adicionamos uma "âncora" de centro invisível mesmo que o chunk real ainda não exista
        self.center_chunks.append(DummyCenter(new_coord[0], new_coord[1]))
        
        self.load_adjacent_chunks(new_coord)

    def load_adjacent_chunks(self, center_coord):
        # Carregamento Dinâmico em Formato Quadrado (Raio R)
        r = self.render_distance_chunks
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                neighbor_x = center_coord[0] + (dx * 16)
                neighbor_z = center_coord[1] + (dz * 16)
                neighbor_coord = (neighbor_x, neighbor_z)
                
                # Se o chunk não está carregado e ainda não foi pedido à outra Thread
                if neighbor_coord not in self.loaded_chunks and neighbor_coord not in self.requested_chunks:
                    self.requested_chunks.add(neighbor_coord)
                    self.chunk_generator.request_chunk(neighbor_x, neighbor_z)

    def update(self, dt):
        self.input()
        
        # 1. Checa se o processador terminou algum chunk novo
        ready_chunks = self.chunk_generator.get_ready_chunks()
        for coord, chunk_data in ready_chunks:
            # Cria a classe principal de Chunk agora que temos os dados
            self.loaded_chunks[coord] = Game_Chunk(self, coord[0], coord[1], chunk_data, self.max_height)
            if coord in self.requested_chunks:
                self.requested_chunks.remove(coord)

        # 2. Atualiza apenas os que já existem
        r = self.render_distance_chunks
        for center in self.center_chunks:
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    chunk_x = center.x + (dx * 16)
                    chunk_z = center.z + (dz * 16)
                    chunk = self.loaded_chunks.get((chunk_x, chunk_z))
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
                    
    def create_chunk(self, x, z):
        self.loaded_chunks.append(Game_Chunk(x, z, max_height=self.max_height))

    def unload_chunk(self, x, z):
        pass

    def create_map(self):
        self.center_chunks = []
        self.loaded_chunks = dict()

        # Apenas definimos o centro inicial, o que vai acionar o carregamento via Thread.
        self.update_chunk((None, None), self.jogador.chunck_coord)
        
        self.entities = []
        self.projectiles = []
        self.gravity = 0.02
        self.air_resistance = 0.5
        self.enemies = []

    def check_collision_with_blocks(self, x, y, z, dims=None, debug=False):
        chunk_coord = (int(math.floor(x / 16)) * 16, int(math.floor(z / 16)) * 16)
        chunk = self.loaded_chunks.get(chunk_coord)
        
        if chunk is None:
            return False
            
        if dims is None:
            block_id = chunk.get_block_global(int(math.floor(x)), int(math.floor(y)), int(math.floor(z)))
            return block_id > 0

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
        # Fecha os processos secundários ao fechar o jogo
        self.chunk_generator.dispose()

    def add_spell(self, spell):
        self.entities.append(spell)

    def add_block(self, x, y, z, block_name):
        pass # Método obsoleto após migração de IDs numéricos
