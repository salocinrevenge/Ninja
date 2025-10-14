import pyray as rl

class Assets_Loader():
    
    def __init__(self, game):
        self.game = game
        self.models_loaded = dict()
        self.textures_loaded = dict()
        self.meshes_loaded = dict()

    def get_model(self,name):
        if name in self.models_loaded.keys():
            return self.models_loaded[name]
        self.models_loaded[name] = rl.load_model(name.encode('utf-8'))
        return self.models_loaded[name]
    
    def get_texture(self,name):
        if name in self.textures_loaded.keys():
            return self.textures_loaded[name]
        self.textures_loaded[name] = rl.load_texture_from_image(rl.load_image(name.encode('utf-8')))
        return self.textures_loaded[name]

    def get_mesh(self, active_faces):
        # active faces is a list of 6 booleans, transforme in a iteger
        key = 0
        for i in range(6):
            if active_faces[i]:
                key |= (1 << i)
        if key in self.meshes_loaded.keys():
            return self.meshes_loaded[key]
        self.meshes_loaded[key] = self.make_cube_mesh(active_faces)
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
            [(-0.5, -0.5,  0.5), (0.5, -0.5,  0.5), (0.5, 0.5,  0.5), (-0.5, 0.5,  0.5)],
            # Trás
            [(0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5)],
            # Direita
            [(0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5)],
            # Esquerda
            [(-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5)],
            # Topo
            [(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5)],
            # Base
            [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5)]
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
        mesh.vertices = rl.ffi.new("float[]", vertices)
        mesh.texcoords = rl.ffi.new("float[]", texcoords)
        mesh.indices = rl.ffi.new("unsigned short[]", indices)

        rl.upload_mesh(mesh, False)
        return mesh


    def clear_all(self):
        for key in self.models_loaded.keys():
            rl.unload_model(self.models_loaded[key])
            self.models_loaded[key] = None
        for key in self.textures_loaded.keys():
            rl.unload_texture(self.textures_loaded[key])
            self.textures_loaded[key] = None

        self.models_loaded = None
        self.textures_loaded = None

