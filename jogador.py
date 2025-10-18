from pyray import Vector3 
import pyray as rl
import math

class Jogador():

    def __init__(self, game):
        self.game = game
        self.pos = Vector3(0, 3, 0)
        self.dims = Vector3(1, 2, 1)
        self.walk_speed = 0.1
        self.vel = Vector3(0, 0, 0)
        self.on_ground = True
        self.lives = 5
        self.time_invulnerable = 0
        self.forward = Vector3(1,0,0)
        self.right = Vector3(0,0,1)
        self.forca_pulo = 0.5
        self.time_invunerability = 100
        self.lives = 5
        self.f3_active = False
        self.yaw = 0

    def update(self,dt):
        if rl.is_key_pressed(rl.KEY_F3):
            self.f3_active = not self.f3_active

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

        self.vel.x += move.x * self.walk_speed
        self.vel.z += move.z * self.walk_speed

        # --- Pulo ---
        if rl.is_key_pressed(rl.KEY_SPACE) and self.on_ground:
            self.vel = rl.vector3_add(self.vel, Vector3(0, self.forca_pulo, 0)) 
            self.on_ground = False

        
        self.vel = rl.vector3_subtract(self.vel, Vector3(0, self.game.gravity, 0))
        future_x = self.pos.x + self.vel.x
        if self.game.check_collision_with_blocks(future_x, self.pos.y, self.pos.z, self.dims):
            future_x = self.pos.x
            self.vel.x = 0
        future_y = self.pos.y + self.vel.y
        if self.game.check_collision_with_blocks(self.pos.x, future_y, self.pos.z, self.dims):
            future_y = self.pos.y
            self.on_ground = True
            self.vel.y = 0
        else:
            self.on_ground = False
        future_z = self.pos.z + self.vel.z
        if self.game.check_collision_with_blocks(self.pos.x, self.pos.y, future_z, self.dims):
            future_z = self.pos.z
            self.vel.z = 0
        self.pos = Vector3(future_x, future_y, future_z)
        self.vel = rl.vector3_multiply(self.vel, Vector3(self.game.air_resistance, 1, self.game.air_resistance))

    def render(self):
        if (self.time_invulnerable//10) % 2 ==0:
            # Se self.pos representa o canto superior, converte para o centro do cubo
            cube_pos = Vector3(
                self.pos.x,   # mover para o centro em X
                self.pos.y + self.dims.y-1,   # do topo para o centro em Y (baixo -> topo)
                self.pos.z    # mover para o centro em Z
            )
            rl.draw_cube_v(cube_pos, self.dims, rl.BLUE)
            

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

        if self.f3_active:
            text = f"Position:\nX: {self.pos.x}\nY: {self.pos.y}\nZ: {self.pos.z} \
                \nLooking at:\nX: {self.game.camera.camera.target.x}\nY: {self.game.camera.camera.target.y}\nZ: {self.game.camera.camera.target.z}\n"
            rl.draw_text(text, 10, 140, 20, (50,50,50,255))
