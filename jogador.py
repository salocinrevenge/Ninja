from pyray import Vector3 
import pyray as rl
import math

class Jogador():

    def __init__(self, game):
        self.game = game
        self.pos = Vector3(0, 1, 0)
        self.dims = Vector3(1, 2, 1)
        self.walk_speed = 0.2
        self.vel = Vector3(0, 0, 0)
        self.on_ground = True
        self.lives = 5
        self.time_invulnerable = 0
        self.forward = Vector3(1,0,0)
        self.right = Vector3(0,0,1)
        self.forca_pulo = 0.35
        self.time_invunerability = 100
        self.lives = 5

    def update(self,dt):
        if self.time_invulnerable > 0:
            self.time_invulnerable -= 1

        # --- Movimento do jogador ---
        move = Vector3(0, 0, 0)
        if rl.is_key_down(rl.KEY_W):
            move.x += self.forward.x
            move.z += self.forward.z
        if rl.is_key_down(rl.KEY_S):
            move.x -= self.forward.x
            move.z -= self.forward.z
        if rl.is_key_down(rl.KEY_A):
            move.x += self.right.x
            move.z += self.right.z
        if rl.is_key_down(rl.KEY_D):
            move.x -= self.right.x
            move.z -= self.right.z

        length = math.sqrt(move.x**2 + move.z**2)
        if length:
            move.x /= length
            move.z /= length

        self.pos.x += move.x * self.walk_speed
        self.pos.z += move.z * self.walk_speed

        # --- Pulo ---
        if rl.is_key_pressed(rl.KEY_SPACE) and on_ground:
            self.vel += Vector3(0, self.forca_pulo, 0)
            on_ground = False

        self.vel -= Vector3(0, self.self.game.gravity, 0)
        self.pos.y += self.vel
        if self.pos.y <= 0:
            self.pos.y = 0
            self.vel = Vector3(0, 0, 0)
            on_ground = True

    def render(self):
        pass

    def hurt(self):
        if self.time_invulnerable > 0:
            return
        self.time_invulnerable = self.time_invunerability
        self.lives-=1
            