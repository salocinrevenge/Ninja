from utils import check_collision
from pyray import Vector3 

class Bullet():

    def __init__(self, pos, vel, player, time_available):
        self.alive = True
        self.pos = pos
        self.vel = vel
        self.player = player
        self.time_available = time_available
        self.time = 0
        self.dims = Vector3(0.5, 0.5, 0.5)

    def update(self,dt):
        if not self.alive:
            return
        self.time+=1
        if self.time > self.time_available:
            self.alive = False

        self.pos += self.vel

        # Colisao com player
        if check_collision(self.player, self):
            self.player.hurt()
            self.alive = False

    def render(self):
        pass