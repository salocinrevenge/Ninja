from enemy import Enemy
import random
import pyray as rl
import math

class SpawnerGame:
    def __init__(self, game):
        self.game = game
        self.timer = 0

        self.times = {1:1, 10:2, 50:3, 100:4, 500:5, 1000:6, 2000: 7, 2500:8}

    def update(self, dt):
        self.timer +=1

        if self.timer in self.times:
            # Spawnar inimigos
            num_enemies = self.times[self.timer]
            for _ in range(num_enemies):
                self.spawn_enemy()

    # def spawn_enemy(self):
    #     Enemy_instance = Enemy(game = self.game,
    #                       pos = rl.Vector3(random.uniform(-10, 10), 3, random.uniform(-10, 10)),
    #                         player=self.game.player)
        
    #     (self, game, pos, player)
    #     self.game.spawn_enemy()
