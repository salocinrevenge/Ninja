from jogador import Jogador
from enemy import Enemy
from pyray import Vector3
from camera import Camera
import random
import math
import pyray as rl

class Game_Manager():
    def __init__(self, motor):
        self.motor = motor
        self.create_map()
        self.jogador = Jogador(self)
        self.camera = Camera(self, self.jogador)
        self.entidades.append(self.jogador)
    
    def render(self):

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(self.camera)
        self.draw_grid(20, 1.0)

        for block in self.static_blocks:
            block.render()
        for entity in self.entities:
            entity.render()
        for proj in self.projectiles:
            proj.render()

        rl.end_mode_3d()

    def update(self, dt):
        for block in self.static_blocks:
            block.update(dt)
        for entity in self.entities:
            entity.update(dt)
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

        self.gravity = 0.2

        # --- Inimigos ---
        self.enemies = []
        for _ in range(3):
            enemy = Enemy(game = self,
                          pos = Vector3(random.uniform(-10, 10), 1, random.uniform(-10, 10)),
                          dir = random.uniform(0, math.tau),
                          speed = 0.05,
                          cooldown= random.uniform(0, 5)
                          )
            self.enemies.append(enemy)
            self.entities.append(enemy)


