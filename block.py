from pyray import load_model, Vector3
import pyray as rl

class Block():
    
    def __init__(self, game, assets_loader, block_name, pos, active_faces = None):
        self.game = game
        self.assets_loader = assets_loader
        self.pos = pos  # centro do mapa, apoiado no chão
        self.block_name = block_name

        # Modelo carregado do blender
        # self.model = assets_loader.get_model(block_name)
        # self.dims = Vector3(1, 1, 1)

        # Modelo criado por textura
        texture = assets_loader.get_texture(block_name) # arquivo 48x64 no mesmo diretório
        # mesh = rl.gen_mesh_cube(1.0, 1.0, 1.0) # cubo 1x1x1
        # self.model = rl.load_model_from_mesh(mesh)
        # self.model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture

        # Cada face: frente, trás, esquerda, direita, topo, base
        if active_faces == None:
            active_faces = [False, False, False, False, True, False]
        self.active_faces = active_faces

        self.model = assets_loader.get_model_cube(self.active_faces, block_name)




    
    def update_face(self, face_index, is_active):
        self.active_faces[face_index] = is_active
        self.model = self.assets_loader.get_model_cube(self.active_faces, self.block_name)




    def update(self,dt):
        pass

    def render(self):
        rl.draw_model(self.model, self.pos, 1.0, rl.WHITE)