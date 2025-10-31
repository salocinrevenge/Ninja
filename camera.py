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
        self.camera_distance = 6.0

    def update(self,dt):
        # --- Alternar visão ---
        
        # --- Movimento da câmera ---
        mouse_delta = rl.get_mouse_delta()
        self.camera_yaw -= mouse_delta.x * 0.003
        self.camera_pitch -= mouse_delta.y * 0.003
        self.camera_pitch = max(-1.5, min(1.5, self.camera_pitch)) #1.2 original

        self.dir_x = math.sin(self.camera_yaw) * math.cos(self.camera_pitch)
        self.dir_y = math.sin(self.camera_pitch)
        self.dir_z = math.cos(self.camera_yaw) * math.cos(self.camera_pitch)

        self.player.forward = rl.Vector3(self.dir_x, self.dir_y, self.dir_z)
        self.player.right = rl.Vector3(math.cos(self.camera_yaw), 0, -math.sin(self.camera_yaw))
        self.player.yaw = self.camera_yaw

        if self.player.third_person:
            cam_offset = rl.Vector3(-self.dir_x * self.camera_distance,
                                 -self.dir_y * self.camera_distance,
                                 -self.dir_z * self.camera_distance)
            self.camera.position = rl.Vector3(
                self.player.pos.x + cam_offset.x,
                self.player.pos.y + self.player.dims.y + cam_offset.y,
                self.player.pos.z + cam_offset.z
            )
        else:
            self.camera.position = rl.Vector3(self.player.pos.x, self.player.pos.y + self.player.dims.y, self.player.pos.z)


        self.camera.target = rl.Vector3(
            self.player.pos.x + self.dir_x,
            self.player.pos.y + 1.5 + self.dir_y,
            self.player.pos.z + self.dir_z
        )
        # self.camera.position = rl.Vector3(0, 10, 0) # debug camera no teto

    def get_block_looked_at_old(self, max_distance=5):

        step = 0.1
        for d in range(int(max_distance / step)):
            check_x = self.camera.position.x + self.dir_x * d * step
            check_y = self.camera.position.y + self.dir_y * d * step
            check_z = self.camera.position.z + self.dir_z * d * step
            if self.game.check_collision_with_blocks(check_x, check_y, check_z, rl.Vector3(0, 0, 0)):
                return (int(math.floor(check_x)), int(math.floor(check_y)+(self.player.dims.y-1)), int(math.floor(check_z)))
        return None

    def get_block_looked_at(self, max_distance=5):
        """
        Retorna o bloco que o jogador está olhando, até uma distância máxima.
        Usa raycast em grade (3D DDA) como o Minecraft.
        """

        # Posição inicial do raio (ponto de visão da câmera)
        x, y, z = self.camera.position.x, self.camera.position.y, self.camera.position.z
        dx, dy, dz = self.dir_x, self.dir_y, self.dir_z

        # Bloco atual (grade inteira)
        bx, by, bz = math.floor(x), math.floor(y), math.floor(z)

        # Direção do passo em cada eixo (+1 ou -1)
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1
        step_z = 1 if dz > 0 else -1

        # Distância até o primeiro limite de bloco em cada eixo
        def next_boundary(pos, dir, block_coord):
            # Retorna distância (float) até o próximo plano inteiro (em unidades de mundo)
            if dir > 0:
                return (block_coord + 1 - pos) / dir
            elif dir < 0:
                return (block_coord - pos) / dir
            else:
                return float('inf')

        t_max_x = next_boundary(x, dx, bx)
        t_max_y = next_boundary(y, dy, by)
        t_max_z = next_boundary(z, dz, bz)

        # Distância entre cruzamentos consecutivos de blocos (em "tempo de raio")
        t_delta_x = abs(1 / dx) if dx != 0 else float('inf')
        t_delta_y = abs(1 / dy) if dy != 0 else float('inf')
        t_delta_z = abs(1 / dz) if dz != 0 else float('inf')

        # Quantos blocos podemos atravessar no raio máximo
        max_steps = int(max_distance * 2)  # fator 2 só pra garantir um alcance suave

        for _ in range(max_steps):
            # --- verifica se há bloco sólido neste voxel ---
            if self.game.check_collision_with_blocks(bx, by, bz, None, debug=True):
                print("Block found at:", bx, by, bz)
                # ↑ função hipotética: retorna True se há um bloco sólido nessa posição (não ar/água)
                return (bx, by, bz)

            # --- avança para o próximo voxel cruzado ---
            if t_max_x < t_max_y and t_max_x < t_max_z:
                bx += step_x
                t_max_x += t_delta_x
            elif t_max_y < t_max_z:
                by += step_y
                t_max_y += t_delta_y
            else:
                bz += step_z
                t_max_z += t_delta_z

            # --- se passou do alcance máximo, encerra ---
            distance = min(t_max_x, t_max_y, t_max_z)
            if distance > max_distance:
                break

        return None



    def render(self):
        pass