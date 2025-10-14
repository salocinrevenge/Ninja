from jogador import Jogador
from enemy import Enemy
from pyray import Vector3
from camera import Camera
from block import Block
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

        for block in self.static_blocks:
            block.render()
        for entity in self.entities:
            entity.render()
        for proj in self.projectiles:
            proj.render()

        rl.end_mode_3d()

        self.jogador.render_hud()

        rl.end_drawing()

    def update(self, dt):
        for block in self.static_blocks:
            block.update(dt)
        for entity in self.entities:
            entity.update(dt)
        self.camera.update(dt)
        new_projectiles = []
        for proj in self.projectiles:
            proj.update(dt)
            if proj.alive:
                new_projectiles.append(proj)
        self.projectiles = new_projectiles

    def create_map(self):
        self.static_blocks = []
        self.entities = []
        self.projectiles = []

        self.gravity = 0.03
        self.air_resistance = 0.5

        for i in range(-20,20):
            for j in range(-20,20):
                self.static_blocks.append(Block(self, self.assets_loader, "cube.glb", Vector3(i+0.5,0.5,j+0.5)))

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

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def dispose(self):
        self.assets_loader.clear_all()



