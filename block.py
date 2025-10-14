from pyray import load_model, Vector3
import pyray as rl

class Block():
    
    def __init__(self, game, assets_loader, block_name, pos):
        self.game = game
        self.assets_loader = assets_loader
        self.pos = pos  # centro do mapa, apoiado no chão

        # Modelo carregado do blender
        # self.model = assets_loader.get_model(block_name)
        # self.dims = Vector3(1, 1, 1)

        # Modelo criado por textura
        texture = assets_loader.get_texture("grass.png") # arquivo 48x64 no mesmo diretório
        # mesh = rl.gen_mesh_cube(1.0, 1.0, 1.0) # cubo 1x1x1
        # self.model = rl.load_model_from_mesh(mesh)
        # self.model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture

        # Cada face: frente, trás, esquerda, direita, topo, base
        self.active_faces = [True, True, True, True, True, True]

        print("assets_loader:", assets_loader)
        mesh = assets_loader.get_mesh(self.active_faces)
        self.model = rl.load_model_from_mesh(mesh)
        self.model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture



    





    def update(self,dt):
        pass

    def render(self):
        rl.draw_model(self.model, self.pos, 1.0, rl.WHITE)