import pyray as rl
import json, os

class Assets_Loader():
    
    def __init__(self, game):
        self.game = game
        self.models_loaded = dict()
        self.textures_loaded = dict()
        self.meshes_loaded = dict()
        self.blocks_path = "assets/blocks/"
        self.hand_positions_path = "assets/hand_positions/"
        self.body_positions_path = "assets/body_positions/"
        self.bodies = {"A": {"None": "head", "A": "sub/brain", "S": "sub/eye", "D":"sub/nose_mouth"}, "S": {"None": "body", "A": "sub/lung", "S": "sub/arm", "D":"sub/hand"}, "D": {"None": "legs", "A": "sub/abdomen", "S": "sub/leg", "D":"sub/foot"}}
        self.load_elements()
        self.load_hand_positions()
        self.load_recipes()

    def get_model(self,name):
        if name in self.models_loaded.keys():
            return self.models_loaded[name]
        self.models_loaded[name] = rl.load_model(name.encode('utf-8'))
        return self.models_loaded[name]
    
    def get_block_texture(self,name):
        return self.get_texture(self.blocks_path + name + ".png")

    def get_texture(self,name):
        if name in self.textures_loaded.keys():
            return self.textures_loaded[name]
        self.textures_loaded[name] = rl.load_texture_from_image(rl.load_image(name.encode('utf-8')))
        return self.textures_loaded[name]
    
    def get_model_block(self, active_faces, name):
        # active faces is a list of 6 booleans, transforme in a iteger
        key = 0
        for i in range(6):
            if active_faces[i]:
                key |= (1 << i)
        key_name = f"{name}_{key}"
        if key_name in self.models_loaded.keys():
            return self.models_loaded[key_name]
        mesh = self.get_mesh(active_faces)
        model = rl.load_model_from_mesh(mesh)
        model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.get_block_texture(name)
        self.models_loaded[key_name] = model
        return self.models_loaded[key_name]

    def get_mesh(self, active_faces):
        # active faces is a list of 6 booleans, transforme in a iteger
        key = 0
        for i in range(6):
            if active_faces[i]:
                key |= (1 << i)
        if key in self.meshes_loaded.keys():
            return self.meshes_loaded[key]
        self.meshes_loaded[key] = self.make_cube_mesh(active_faces).mesh
        return self.meshes_loaded[key]
        
    def make_cube_mesh(self, active_faces):
        """Gera um mesh de cubo com apenas as faces ativas (True/False)."""
        # Lista de vértices (x,y,z) e UVs (u,v)
        vertices = []
        texcoords = []
        indices = []
        
        # Ordem das faces: frente, trás, direita, esquerda, topo, base
        face_positions = [
            # Frente
            [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],
            # Trás
            [(1, 0, 0), (0, 0, 0), (0, 1, 0), (1, 1, 0)],
            # Direita
            [(1, 0, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
            # Esquerda
            [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)],
            # Topo
            [(0, 1, 1), (1, 1, 1), (1, 1, 0), (0, 1, 0)],
            # Base
            [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)]
        ]
        
        # UV padrão para a face inteira
        uv = [(0, 1), (1, 1), (1, 0), (0, 0)]

        vertex_count = 0
        for face_idx, active in enumerate(active_faces):
            if not active:
                continue
            # Adiciona vértices e UVs
            for v_idx in range(4):
                x, y, z = face_positions[face_idx][v_idx]
                u, v = uv[v_idx]
                vertices.extend([x, y, z])
                texcoords.extend([u, v])
            # Adiciona índices (dois triângulos)
            indices.extend([vertex_count, vertex_count+1, vertex_count+2,
                            vertex_count, vertex_count+2, vertex_count+3])
            vertex_count += 4

        # Cria o mesh
        mesh = rl.Mesh()
        mesh.vertexCount = len(vertices) // 3
        mesh.triangleCount = len(indices) // 3

        # --- Alocação dos buffers
        vertices_buf = rl.ffi.new("float[]", vertices)
        texcoords_buf = rl.ffi.new("float[]", texcoords)
        indices_buf = rl.ffi.new("unsigned short[]", indices)

        mesh.vertices = vertices_buf
        mesh.texcoords = texcoords_buf
        mesh.indices = indices_buf

        rl.upload_mesh(mesh, True)

        return MeshWrapper(mesh, vertices_buf, texcoords_buf, indices_buf)

    def load_elements(self):
        elems_path = "assets/elements.json"
        with open(elems_path, "r", encoding="utf-8") as f:
            self.elements_properities = json.load(f)

    def load_hand_positions(self):
        hand_pos_path = "assets/hand_pos_prop.json"
        with open(hand_pos_path, "r", encoding="utf-8") as f:
            self.hand_positions_properties = json.load(f)

    def load_recipes(self):
        recipes_path = "assets/recipes.json"
        with open(recipes_path, "r", encoding="utf-8") as f:
            self.loaded_recipes = json.load(f)

    def color_element(self, element):
        if element in self.elements_properities:
            return True, self.elements_properities[element]["cor"]
        return False, self.elements_properities["None"]["cor"]


    def clear_all(self):
        return
        print("Clearing all loaded assets...")
        print(len(self.models_loaded), "models,",
              len(self.textures_loaded), "textures,",
              len(self.meshes_loaded), "meshes.")
        for key in self.models_loaded.keys():
            rl.unload_model(self.models_loaded[key])
            self.models_loaded[key] = None
        for key in self.textures_loaded.keys():
            rl.unload_texture(self.textures_loaded[key])
            self.textures_loaded[key] = None
        for key in self.meshes_loaded.keys():
            rl.unload_mesh(self.meshes_loaded[key])
            self.meshes_loaded[key] = None

        self.models_loaded = None
        self.textures_loaded = None
        self.meshes_loaded = None


class MeshWrapper:
    def __init__(self, mesh, vertices_buf, texcoords_buf, indices_buf):
        self.mesh = mesh
        self.vertices_buf = vertices_buf
        self.texcoords_buf = texcoords_buf
        self.indices_buf = indices_buf