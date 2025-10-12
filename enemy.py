from pyray import Vector3 
from bullet import Bullet 
from utils import check_collision
import math
import random

class Enemy():

    def __init__(self, game, pos, dir, speed, cooldown, player):
        self.game = game
        self.pos = pos
        self.dir = dir
        self.speed = speed
        self.cooldown = cooldown
        self.player = player
        self.counter = 0

    def update(self,dt):
        self.pos.x += math.cos(self.dir) * self.speed
        self.pos.z += math.sin(self.dir) * self.speed
        if abs(self.pos.x) > 19 or abs(self.pos.z) > 19:
            self.dir += math.pi / 2
        self.counter += 1
        if self.counter >= self.cooldown:
            self.counter = random.uniform(0, 3)
            dir_to_player = Vector3(
                self.player.pos.x - self.pos.x,
                0,
                self.player.pos.z - self.pos.z
            )
            d = math.sqrt(dir_to_player.x**2 + dir_to_player.z**2)
            if d != 0:
                dir_to_player.x /= d
                dir_to_player.z /= d
            self.game.add_projectile(Bullet(Vector3(self.pos.x, 1.5, self.pos.z), Vector3(dir_to_player.x * 0.3, 0, dir_to_player.z * 0.3), 5))



        # Colision with player
        if check_collision(self.player, self):
            self.player.hurt()

    def render(self):
        pass