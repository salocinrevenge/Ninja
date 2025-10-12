import pyray as rl
import math

class Camera():
    
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.camera = rl.Camera3D()
        self.camera.up = rl.Vector3(0, 1, 0)
        self.camera.fovy = 90
        self.camera_pitch = -0.3
        self.camera_yaw = 0
        self.third_person = False
        self.camera_distance = 6.0

    def update(self,dt):
        # --- Alternar visão ---
        if rl.is_key_pressed(rl.KEY_F5):
            self.third_person = not self.third_person
        
        # --- Movimento da câmera ---
        mouse_delta = rl.get_mouse_delta()
        camera_yaw -= mouse_delta.x * 0.003
        camera_pitch -= mouse_delta.y * 0.003
        camera_pitch = max(-1.2, min(1.2, camera_pitch))

        dir_x = math.sin(camera_yaw) * math.cos(camera_pitch)
        dir_y = math.sin(camera_pitch)
        dir_z = math.cos(camera_yaw) * math.cos(camera_pitch)

        self.player.forward = rl.Vector3(dir_x, dir_y, dir_z)
        self.player.right = rl.Vector3(math.cos(camera_yaw), 0, -math.sin(camera_yaw))

        if self.third_person:
            cam_offset = rl.Vector3(-dir_x * self.camera_distance,
                                 -dir_y * self.camera_distance,
                                 -dir_z * self.camera_distance)
            self.camera.position = rl.Vector3(
                self.player.pos.x + cam_offset.x,
                self.player.pos.y + 2 + cam_offset.y,
                self.player.pos.z + cam_offset.z
            )
        else:
            self.camera.position = rl.Vector3(self.player.pos.x, self.player.pos.y + 1.5, self.player.pos.z)

        self.camera.target = rl.Vector3(
            self.player.pos.x + dir_x,
            self.player.pos.y + 1.5 + dir_y,
            self.player.pos.z + dir_z
        )



    def render(self):
        pass