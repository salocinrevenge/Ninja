import pyray

class Player:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SIZE, PLAYER_SPEED):
        self.rect = pyray.Rectangle(
            SCREEN_WIDTH / 2 - PLAYER_SIZE / 2,
            SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.PLAYER_SPEED = PLAYER_SPEED
        self.color = pyray.WHITE
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            return
        # Movimento com WASD
        if pyray.is_key_down(pyray.KEY_W):
            self.rect.y -= self.PLAYER_SPEED
        if pyray.is_key_down(pyray.KEY_S):
            self.rect.y += self.PLAYER_SPEED
        if pyray.is_key_down(pyray.KEY_A):
            self.rect.x -= self.PLAYER_SPEED
        if pyray.is_key_down(pyray.KEY_D):
            self.rect.x += self.PLAYER_SPEED
        # Limites da tela
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.SCREEN_WIDTH - self.rect.width:
            self.rect.x = self.SCREEN_WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > self.SCREEN_HEIGHT - self.rect.height:
            self.rect.y = self.SCREEN_HEIGHT - self.rect.height
    def draw(self):
        pyray.draw_rectangle_rec(self.rect, self.color)