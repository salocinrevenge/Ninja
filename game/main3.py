import pyray
import math
import random
import asyncio
from other_file import Player

# /// script
# dependencies = [
# "cffi",
# "raylib"
# ]
# ///

# --- Estruturas (Classes) ---


class Bullet:
    def __init__(self, x, y, direction_x, direction_y, bullet_size, bullet_speed, screen_width, screen_height):
        self.rect = pyray.Rectangle(x, y, bullet_size, bullet_size)
        self.color = pyray.RED
        self.bullet_size = bullet_size
        self.bullet_speed = bullet_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Normaliza a direção para garantir velocidade constante
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length != 0:
            self.direction_x = direction_x / length
            self.direction_y = direction_y / length
        else:
            self.direction_x = 0
            self.direction_y = 0

    def update(self):
        self.rect.x += self.direction_x * self.bullet_speed
        self.rect.y += self.direction_y * self.bullet_speed

    def draw(self):
        pyray.draw_rectangle_rec(self.rect, self.color)

    def is_outside(self):
        return (
            self.rect.x < -self.bullet_size or
            self.rect.x > self.screen_width or
            self.rect.y < -self.bullet_size or
            self.rect.y > self.screen_height
        )

class Enemy:
    def __init__(self, screen_width, screen_height, enemy_size, enemy_speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemy_size = enemy_size
        self.enemy_speed = enemy_speed
        self.rect = pyray.Rectangle(
            random.uniform(0, screen_width - enemy_size),
            random.uniform(0, screen_height - enemy_size),
            enemy_size,
            enemy_size
        )
        self.color = pyray.GREEN
        self.direction_x = random.uniform(-1, 1)
        self.direction_y = random.uniform(-1, 1)
        self.bullet_timer = 0.0

    def update(self, delta_time):
        # Movimento aleatório (bouncing)
        self.rect.x += self.direction_x * self.enemy_speed
        self.rect.y += self.direction_y * self.enemy_speed
        # Limites da tela (inverte a direção ao tocar a borda)
        if self.rect.x < 0 or self.rect.x > self.screen_width - self.rect.width:
            self.direction_x *= -1
        if self.rect.y < 0 or self.rect.y > self.screen_height - self.rect.height:
            self.direction_y *= -1

    def draw(self):
        pyray.draw_rectangle_rec(self.rect, self.color)

class Motor:

    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.TITLE = "Raylib Python Web Game"
        self.FPS = 60
        self.PLAYER_SIZE = 20
        self.PLAYER_SPEED = 4.0
        self.MAX_ENEMIES = 3
        self.ENEMY_SIZE = 25
        self.ENEMY_SPEED = 2.0
        self.BULLET_SIZE = 5
        self.BULLET_SPEED = 5.0
        self.BULLET_SPAWN_RATE = 0.5  # Balas por segundo

    # --- Funções de Jogo ---
    def enemy_shoot_bullets(self, enemy, bullets_list, delta_time, bullet_spawn_rate, bullet_size, bullet_speed, screen_width, screen_height):
        """Lógica para o inimigo atirar em 8 direções."""
        # Atualiza o timer do tiro
        enemy.bullet_timer += delta_time
        # Taxa de tiro (a cada 1/BULLET_SPAWN_RATE segundos)
        if enemy.bullet_timer >= 1.0 / bullet_spawn_rate:
            enemy.bullet_timer = 0.0
            center_x = enemy.rect.x + enemy.rect.width / 2
            center_y = enemy.rect.y + enemy.rect.height / 2
            # Direções de tiro (8 direções)
            directions = [
                (1, 0), (0, 1), (-1, 0), (0, -1),  # Cardinais
                (1, 1), (-1, 1), (1, -1), (-1, -1)  # Diagonais
            ]
            for dir_x, dir_y in directions:
                # Cria a bala no centro do inimigo
                bullet = Bullet(
                    center_x - bullet_size / 2,
                    center_y - bullet_size / 2,
                    dir_x,
                    dir_y,
                    bullet_size,
                    bullet_speed,
                    screen_width,
                    screen_height
                )
                bullets_list.append(bullet)

    async def run(self):
        # Inicialização
        pyray.set_config_flags(pyray.FLAG_WINDOW_RESIZABLE)
        pyray.init_window(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.TITLE)
        if not pyray.is_window_ready():
            print("Falha ao inicializar janela Raylib!")
        pyray.set_target_fps(self.FPS)
        pyray.disable_cursor()
        player = Player(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.PLAYER_SIZE, self.PLAYER_SPEED)
        enemies = [Enemy(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.ENEMY_SIZE, self.ENEMY_SPEED) for _ in range(self.MAX_ENEMIES)]
        bullets = []
        game_over = False
        rotation_x = 0.0  # Ângulo de rotação do cubo no eixo X
        rotation_y = 0.0  # Ângulo de rotação do cubo no eixo Y
        mouse_sensitivity = 0.5  # Sensibilidade do mouse

        # --- Camera 3D para debug (não desenha nada) ---
        camera = pyray.Camera3D()
        camera.position = pyray.Vector3(0.0, 10.0, 10.0)
        camera.target = pyray.Vector3(0.0, 0.0, 0.0)
        camera.up = pyray.Vector3(0.0, 1.0, 0.0)
        camera.fovy = 45.0
        # camera.projection = pyray.CAMERA_PERSPECTIVE

        # Loop Principal do Jogo
        while not pyray.window_should_close():
            delta_time = pyray.get_frame_time()

            # --- 1. Atualização ---
            if not game_over:
                player.update()
                # Atualiza inimigos e faz eles atirarem
                for enemy in enemies:
                    enemy.update(delta_time)
                    self.enemy_shoot_bullets(enemy, bullets, delta_time, self.BULLET_SPAWN_RATE, self.BULLET_SIZE, self.BULLET_SPEED, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                # Atualiza balas (remove as que saem da tela)
                i = 0
                while i < len(bullets):
                    bullets[i].update()
                    if bullets[i].is_outside():
                        bullets.pop(i)
                    else:
                        i += 1
                # Colisão: Jogador vs Balas
                player_rect = player.rect
                for bullet in bullets:
                    bullet_rect = bullet.rect
                    if pyray.check_collision_recs(player_rect, bullet_rect):
                        game_over = True
                        player.color = pyray.DARKGRAY  # Mudar cor ao perder
                        break  # Sai do loop de balas
            # Atualiza ângulos de rotação do cubo com base no movimento do mouse
            mouse_delta = pyray.get_mouse_delta()
            rotation_x += mouse_delta.y * mouse_sensitivity
            rotation_y += mouse_delta.x * mouse_sensitivity

            # --- 2. Desenho ---
            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)

            # --- Modo 3D de debug (não desenha nada dentro) ---
            pyray.begin_mode_3d(camera)
            # Desenha um cubo 3D rotacionando no centro da tela
            pyray.rl_push_matrix()
            pyray.rl_rotatef(rotation_y, 0.0, 1.0, 0.0)  # Rotação em torno do eixo Y
            pyray.rl_rotatef(rotation_x, 1.0, 0.0, 0.0)  # Rotação em torno do eixo X
            pyray.draw_cube(pyray.Vector3(0.0, 0.0, 0.0), 2.0, 2.0, 2.0, pyray.BLUE)
            pyray.rl_pop_matrix()
            pyray.end_mode_3d()

            # Desenha elementos do jogo (2D)
            player.draw()
            for enemy in enemies:
                enemy.draw()
            for bullet in bullets:
                bullet.draw()
            # Desenha a mensagem Game Over
            if game_over:
                text = "GAME OVER! Desvie era o objetivo. Pressione [R] para Recomeçar."
                text_size = pyray.measure_text(text, 20)
                pyray.draw_text(
                    text,
                    self.SCREEN_WIDTH // 2 - text_size // 2,
                    self.SCREEN_HEIGHT // 2 - 10,
                    20,
                    pyray.WHITE
                )
                # Lógica de reinício
                if pyray.is_key_pressed(pyray.KEY_R):
                    player = Player(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.PLAYER_SIZE, self.PLAYER_SPEED)
                    enemies = [Enemy(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.ENEMY_SIZE, self.ENEMY_SPEED) for _ in range(self.MAX_ENEMIES)]
                    bullets = []
                    game_over = False
            # Instruções
            pyray.draw_text(
                "Mova com WASD. Desvie dos projéteis vermelhos.",
                10,
                10,
                10,
                pyray.GRAY
            )
            pyray.end_drawing()
            await asyncio.sleep(0)

        # Desinicialização
        pyray.close_window()

if __name__ == '__main__':
    motor = Motor()
    asyncio.run(motor.run())

# venv no windows:
# Set-ExecutionPolicy RemoteSigned -Scope Process
# .\venv\Scripts\activate
# pip install raylib
# python3.12 -m pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl --git my_project
# ou só
# pygbag --ume_block 0 --template noctx.tmpl .


# em game: python -m pygbag --template noctx.tmpl --PYBUILD 3.12 --ume_block 0 --git .
# e tbm python main.py
# Essa coisa ta compilando, testar desenhar o meu jogo sem textura e transformar pouco a pouco o codigo desse no meu