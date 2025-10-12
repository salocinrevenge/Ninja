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
        if rl.is_key_pressed(rl.KEY_SPACE) and self.on_ground:
            self.vel = rl.vector3_add(self.vel, Vector3(0, self.forca_pulo, 0)) 
            self.on_ground = False

        
        self.vel = rl.vector3_subtract(self.vel, Vector3(0, self.game.gravity, 0))
        self.pos = rl.vector3_add(self.pos, self.vel)
        if self.pos.y <= 1:
            self.pos.y = 1
            self.vel = Vector3(0, 0, 0)
            self.on_ground = True

    def render(self):
        if (self.time_invulnerable//10) % 2 ==0:
             rl.draw_cube(self.pos, self.dims.x, self.dims.y, self.dims.z, rl.BLUE)

    def hurt(self):
        if self.time_invulnerable > 0:
            return
        self.time_invulnerable = self.time_invunerability
        self.lives-=1
            
    def render_hud(self):
        for i in range(self.lives):
            x = 20 + i * 35
            y = 20
            rl.draw_rectangle(x, y, 30, 30, rl.RED)

        # invulnerabilidade
        if self.time_invulnerable>0:
            rl.draw_text("INVULNERÁVEL", 20, 60, 25, rl.GOLD)

        rl.draw_text("F5 alterna visão", 10, 100, 20, rl.GRAY)