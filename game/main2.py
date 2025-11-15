import pyray
import math
import random
import asyncio

# /// script
# dependencies = [
# "cffi",
# "raylib"
# ]
# ///


# --- Configurações do Jogo ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
TITLE = "Raylib Python Web Game"
FPS = 60
PLAYER_SIZE = 20
PLAYER_SPEED = 4.0
MAX_ENEMIES = 3
ENEMY_SIZE = 25
ENEMY_SPEED = 2.0
BULLET_SIZE = 5
BULLET_SPEED = 5.0
BULLET_SPAWN_RATE = 0.5  # Balas por segundo

# --- Estruturas (Classes) ---
class Player:
    def __init__(self):
        self.rect = pyray.Rectangle(
            SCREEN_WIDTH / 2 - PLAYER_SIZE / 2,
            SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
        self.color = pyray.WHITE
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            return
        # Movimento com WASD
        if pyray.is_key_down(pyray.KEY_W):
            self.rect.y -= PLAYER_SPEED
        if pyray.is_key_down(pyray.KEY_S):
            self.rect.y += PLAYER_SPEED
        if pyray.is_key_down(pyray.KEY_A):
            self.rect.x -= PLAYER_SPEED
        if pyray.is_key_down(pyray.KEY_D):
            self.rect.x += PLAYER_SPEED
        # Limites da tela
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def draw(self):
        pyray.draw_rectangle_rec(self.rect, self.color)

class Bullet:
    def __init__(self, x, y, direction_x, direction_y):
        self.rect = pyray.Rectangle(x, y, BULLET_SIZE, BULLET_SIZE)
        self.color = pyray.RED
        # Normaliza a direção para garantir velocidade constante
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length != 0:
            self.direction_x = direction_x / length
            self.direction_y = direction_y / length
        else:
            self.direction_x = 0
            self.direction_y = 0

    def update(self):
        self.rect.x += self.direction_x * BULLET_SPEED
        self.rect.y += self.direction_y * BULLET_SPEED

    def draw(self):
        pyray.draw_rectangle_rec(self.rect, self.color)

    def is_outside(self):
        return (
            self.rect.x < -BULLET_SIZE or
            self.rect.x > SCREEN_WIDTH or
            self.rect.y < -BULLET_SIZE or
            self.rect.y > SCREEN_HEIGHT
        )

class Enemy:
    def __init__(self):
        self.rect = pyray.Rectangle(
            random.uniform(0, SCREEN_WIDTH - ENEMY_SIZE),
            random.uniform(0, SCREEN_HEIGHT - ENEMY_SIZE),
            ENEMY_SIZE,
            ENEMY_SIZE
        )
        self.color = pyray.GREEN
        self.direction_x = random.uniform(-1, 1)
        self.direction_y = random.uniform(-1, 1)
        self.bullet_timer = 0.0

    def update(self, delta_time):
        # Movimento aleatório (bouncing)
        self.rect.x += self.direction_x * ENEMY_SPEED
        self.rect.y += self.direction_y * ENEMY_SPEED
        # Limites da tela (inverte a direção ao tocar a borda)
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.direction_x *= -1
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.direction_y *= -1

    def draw(self):
        pyray.draw_rectangle_rec(self.rect, self.color)

# --- Funções de Jogo ---
def enemy_shoot_bullets(enemy, bullets_list, delta_time):
    """Lógica para o inimigo atirar em 8 direções."""
    # Atualiza o timer do tiro
    enemy.bullet_timer += delta_time
    # Taxa de tiro (a cada 1/BULLET_SPAWN_RATE segundos)
    if enemy.bullet_timer >= 1.0 / BULLET_SPAWN_RATE:
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
                center_x - BULLET_SIZE / 2,
                center_y - BULLET_SIZE / 2,
                dir_x,
                dir_y
            )
            bullets_list.append(bullet)

async def main():
    # Inicialização
    pyray.set_config_flags(pyray.FLAG_WINDOW_RESIZABLE)
    pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    if not pyray.is_window_ready():
        print("Falha ao inicializar janela Raylib!")
    pyray.set_target_fps(FPS)
    player = Player()
    enemies = [Enemy() for _ in range(MAX_ENEMIES)]
    bullets = []
    game_over = False
    print("Jogo iniciado com sucesso!TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    # Loop Principal do Jogo
    while not pyray.window_should_close():
        delta_time = pyray.get_frame_time()

        # --- 1. Atualização ---
        if not game_over:
            player.update()
            # Atualiza inimigos e faz eles atirarem
            for enemy in enemies:
                enemy.update(delta_time)
                enemy_shoot_bullets(enemy, bullets, delta_time)
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

        # --- 2. Desenho ---
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        # Desenha elementos do jogo
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
                SCREEN_WIDTH // 2 - text_size // 2,
                SCREEN_HEIGHT // 2 - 10,
                20,
                pyray.WHITE
            )
            # Lógica de reinício
            if pyray.is_key_pressed(pyray.KEY_R):
                player = Player()
                enemies = [Enemy() for _ in range(MAX_ENEMIES)]
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
    asyncio.run(main())

# venv no windows:
# Set-ExecutionPolicy RemoteSigned -Scope Process
# .\venv\Scripts\activate
# pip install raylib
# python3.12 -m pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl --git my_project
# ou só
# pygbag --ume_block 0 --template noctx.tmpl .