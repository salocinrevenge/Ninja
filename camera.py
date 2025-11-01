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
        self.camera_pitch = max(-1.570775, min(1.570775, self.camera_pitch)) #1.2 original

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
                self.player.pos.y + self.player.eye_height + cam_offset.y,
                self.player.pos.z + cam_offset.z
            )
        else:
            self.camera.position = rl.Vector3(self.player.pos.x, self.player.pos.y + self.player.eye_height, self.player.pos.z)


        self.camera.target = rl.Vector3(
            self.player.pos.x + self.dir_x,
            self.player.pos.y + self.player.eye_height + self.dir_y,
            self.player.pos.z + self.dir_z
        )
        # self.camera.position = rl.Vector3(0, 10, 0) # debug camera no teto

    def get_block_looked_at(self, max_distance=10):
        """
        Retorna o bloco que o jogador está olhando, até uma distância máxima.
        Usa raycast em grade (3D DDA) como o Minecraft.
        """
        # Posição inicial do raio (centro da tela/target da câmera)
        x = self.player.pos.x
        y = self.player.pos.y + self.player.eye_height  # 1.5 é a altura dos olhos
        z = self.player.pos.z
        
        # Direção do raio (igual à direção da câmera)
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

        # Distância entre cruzamentos consecutivos de blocos
        t_delta_x = abs(1 / dx) if dx != 0 else float('inf')
        t_delta_y = abs(1 / dy) if dy != 0 else float('inf')
        t_delta_z = abs(1 / dz) if dz != 0 else float('inf')

        max_steps = int(max_distance * 2)

        # Se o jogador começar dentro de um bloco sólido, detectamos isso primeiro.
        if self.game.check_collision_with_blocks(bx, by, bz, None, debug=True):
            # Estamos dentro do bloco inicial — não há face definida
            return (bx, by, bz, None)

        for _ in range(max_steps):
            # Determina qual eixo será atravessado em seguida (menor t_max)
            if t_max_x < t_max_y and t_max_x < t_max_z:
                bx += step_x
                last_axis = 'x'
                t_max_x += t_delta_x
            elif t_max_y < t_max_z:
                by += step_y
                last_axis = 'y'
                t_max_y += t_delta_y
            else:
                bz += step_z
                last_axis = 'z'
                t_max_z += t_delta_z

            # Distância percorrida até o ponto atual do raio
            distance = min(t_max_x, t_max_y, t_max_z)
            if distance > max_distance:
                break

            # Checa colisão no bloco que acabamos de entrar
            if self.game.check_collision_with_blocks(bx, by, bz, None, debug=True):
                # Determina a face com base no último eixo atravessado e no sinal do passo
                if last_axis == 'x':
                    face = 'west' if step_x > 0 else 'east'
                elif last_axis == 'y':
                    face = 'bottom' if step_y > 0 else 'top'
                else:  # 'z'
                    face = 'south' if step_z > 0 else 'north'
                return (bx, by, bz, face)

        return None



    def render(self):
        pass