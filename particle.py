import pyray as rl
import random

class Particle_Manager:
    def __init__(self, game, color, pos, velocity, time_to_produce, time_to_live):
        self.game = game
        self.particles = []
        self.color = color
        self.time_to_produce = time_to_produce
        self.counter = 0
        self.time_to_live = time_to_live
        self.pos = pos
        self.velocity = velocity

    def create_particle(self, position, velocity, lifetime, color):
        self.particles.append(Particle(position, velocity, lifetime, color))

    def update_particles(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.is_alive()]

    def render(self):
        for particle in self.particles:
            particle.render()

    def update(self, dt):
        self.update_particles(dt)
        self.counter += 1
        if self.counter >= self.time_to_produce:
            self.counter = 0
            position = rl.Vector2(self.pos.x + random.uniform(-1, 1), self.pos.y + random.uniform(-1, 1))
            velocity = rl.Vector2(self.velocity.x + random.uniform(-1, 1), self.velocity.y + random.uniform(-1, 1))
            self.create_particle(position, velocity, self.time_to_live*random.uniform(0.5, 2), self.color)
        

class Particle:
    def __init__(self, position, velocity, lifetime, cor):
        self.position = position
        self.velocity = velocity
        self.lifetime = lifetime
        self.color = cor

    def update(self, dt):
        self.position = rl.Vector2(self.position.x + self.velocity.x, self.position.y + self.velocity.y)
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0

    def render(self):
        rl.draw_pixel(int(self.position.x), int(self.position.y), self.color)

