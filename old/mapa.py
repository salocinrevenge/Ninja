from jogador import Jogador

class Mapa():
    def __init__(self):
        self.mapa = []
        self.entidades = []
        self.jogador = Jogador()
        self.entidades.append(self.jogador)
    
    def render(self, screen):
        for entidade in self.entidades:
            entidade.render(screen)

    def tick(self):
        for entidade in self.entidades:
            entidade.tick()
    
    def input(self, tecla):
        self.jogador.input(tecla)