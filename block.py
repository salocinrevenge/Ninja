from pyray import load_model, Vector3

class Block():
    
    def __init__(self, game, assets_loader, block_name):
        self.game = game
        self.assetsLoader = assets_loader
        self.model = assets_loader(block_name)
        self.pos = Vector3(0.0, 0.5, 0.0)  # centro do mapa, apoiado no chão
        self.dims = Vector3(1, 1, 1)


    def update(self,dt):
        pass

    def render(self):
        pass