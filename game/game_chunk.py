import pyray as rl
import ctypes



class SubChunk:
    def __init__(self, parent_chunk, local_y_index):
        self.parent = parent_chunk
        self.game = parent_chunk.game
        self.local_y_index = local_y_index # Índice vertical (ex: 0 = y:0 a 15, 1 = y:16 a 31)
        self.world_y_offset = local_y_index * 16
        
        # Array 3D de IDs de blocos (0 = Ar, 1 = Grama, 2 = Terra...)
        # Usar listas 1D simulando 3D é ainda mais rápido na CPU: index = x + z*16 + y*256
        self.blocks = [0] * (16 * 16 * 16) 
        
        self.model = None
        self.is_dirty = True # Indica se a malha precisa ser refeita

    # Definimos as direções das faces para facilitar a geração da malha
    FACES = [
        # Normal,     Vértices (x, y, z) em coordenadas locais
        # Topo (y+1)
        ((0, 1, 0),  [(0,1,0), (0,1,1), (1,1,1), (1,1,0)]),
        # Base (y-1)
        ((0, -1, 0), [(0,0,1), (0,0,0), (1,0,0), (1,0,1)]),
        # Direita (x+1)
        ((1, 0, 0),  [(1,0,1), (1,0,0), (1,1,0), (1,1,1)]),
        # Esquerda (x-1)
        ((-1, 0, 0), [(0,0,0), (0,0,1), (0,1,1), (0,1,0)]),
        # Frente (z+1)
        ((0, 0, 1),  [(0,0,1), (1,0,1), (1,1,1), (0,1,1)]),
        # Trás (z-1)
        ((0, 0, -1), [(1,0,0), (0,0,0), (0,1,0), (1,1,0)])
    ]

    def get_texture_uv(self, block_id, face_idx):
        # Quantidade de texturas por linha/coluna no seu arquivo de atlas
        # Se o seu atlas tem 16 texturas de largura, o tamanho é 16.0
        ATLAS_COLS = 16.0
        TILE_SIZE = 1.0 / ATLAS_COLS
        
        # Mapeamento (Coluna x, Linha y) no Atlas
        # face_idx: 0=Topo, 1=Base, 2=Dir, 3=Esq, 4=Frente, 5=Trás
        if block_id == 1: # Grama
            if face_idx == 0:   
                tx, ty = 0, 0 # Posição da textura do Topo da Grama no atlas
            elif face_idx == 1: 
                tx, ty = 2, 0 # Posição da Terra (Base)
            else:               
                tx, ty = 1, 0 # Lados da Grama
        elif block_id == 2: # Terra
            tx, ty = 2, 0
        else:
            tx, ty = 0, 0 # Textura padrão para IDs desconhecidos

        # Calcula os pontos (entre 0.0 e 1.0) baseados no tamanho do tile
        u0 = tx * TILE_SIZE
        v0 = ty * TILE_SIZE
        u1 = u0 + TILE_SIZE
        v1 = v0 + TILE_SIZE

        # Retorna os UVs para os 4 vértices da face
        return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]

    def get_block(self, x, y, z):
        if 0 <= x < 16 and 0 <= y < 16 and 0 <= z < 16:
            return self.blocks[x + z * 16 + y * 256]
        return 0 # Ar se fora dos limites locais

    def set_block(self, x, y, z, block_id):
        if 0 <= x < 16 and 0 <= y < 16 and 0 <= z < 16:
            self.blocks[x + z * 16 + y * 256] = block_id
            self.is_dirty = True

    def build_mesh(self):
        vertices = []
        texcoords = []
        indices = []
        index_count = 0

        # Oclusão de Faces (Simple Meshing)
        for y in range(16):
            for z in range(16):
                for x in range(16):
                    block_id = self.get_block(x, y, z)
                    if block_id == 0:
                        continue # Ar não desenha

                    # Checar vizinhos para cada face
                    for face_idx, (normal, face_verts) in enumerate(self.FACES):
                        nx, ny, nz = x + normal[0], y + normal[1], z + normal[2]
                        
                        # Verifica se o vizinho é transparente/ar
                        neighbor_id = self.parent.get_block_global(
                            self.parent.x + nx, 
                            self.world_y_offset + ny, 
                            self.parent.z + nz
                        )

                        if neighbor_id == 0: # Adiciona a face apenas se tocar no ar
                            
                            # Busca as coordenadas UV corretas do Atlas
                            uvs = self.get_texture_uv(block_id, face_idx)
                            
                            for i, v in enumerate(face_verts):
                                vertices.extend([v[0] + x, v[1] + y, v[2] + z])
                                texcoords.extend([uvs[i][0], uvs[i][1]])

                            indices.extend([index_count, index_count+1, index_count+2, 
                                            index_count, index_count+2, index_count+3])
                            index_count += 4

        self.upload_mesh(vertices, texcoords, indices)
        self.is_dirty = False

    def upload_mesh(self, vertices, texcoords, indices):
        # 1. Limpeza Segura do Modelo Antigo
        if self.model is not None:
            # Raylib armadilha: O UnloadModel apaga a textura vinculada da placa de vídeo!
            # Para não apagar a sua textura global do assets_loader, removemos a referência antes:
            self.model.materials[0].maps[rl.MATERIAL_MAP_ALBEDO].texture = rl.Texture(0, 1, 1, 1, 1)
            
            rl.unload_model(self.model)
            self.model = None

        if not vertices:
            return

        mesh = rl.Mesh()
        mesh.vertexCount = len(vertices) // 3
        mesh.triangleCount = len(indices) // 3

        # 2. Alocação Nativa C (Impede o crash silencioso)
        # Ao invés de criar a memória no Python, criamos na Raylib para ela poder gerenciar e limpar.
        v_size = len(vertices) * rl.ffi.sizeof("float")
        t_size = len(texcoords) * rl.ffi.sizeof("float")
        i_size = len(indices) * rl.ffi.sizeof("unsigned short")

        mesh.vertices = rl.ffi.cast("float *", rl.mem_alloc(v_size))
        mesh.texcoords = rl.ffi.cast("float *", rl.mem_alloc(t_size))
        mesh.indices = rl.ffi.cast("unsigned short *", rl.mem_alloc(i_size))

        # 3. Copiando os dados do Python para a memória da Raylib
        v_data = rl.ffi.new("float[]", vertices)
        t_data = rl.ffi.new("float[]", texcoords)
        i_data = rl.ffi.new("unsigned short[]", indices)

        rl.ffi.memmove(mesh.vertices, v_data, v_size)
        rl.ffi.memmove(mesh.texcoords, t_data, t_size)
        rl.ffi.memmove(mesh.indices, i_data, i_size)

        # Envia a malha para a Placa de Vídeo
        rl.upload_mesh(rl.ffi.addressof(mesh), False)
        
        # Cria o modelo
        self.model = rl.load_model_from_mesh(mesh)
        
        # 4. Solução do "Tudo Branco/Preto" usando função nativa da Raylib
        try:
            # Pegue o seu atlas do gerenciador de assets
            textura = self.game.assets_loader.get_block_texture("atlas")
            
            # Força a associação da textura ao material usando ponteiros CFFI
            rl.set_material_texture(
                rl.ffi.addressof(self.model.materials[0]), 
                rl.MATERIAL_MAP_ALBEDO, 
                textura
            )
        except Exception as e:
            print("Não foi possível puxar a textura do atlas:", e)

    def render(self):
        if self.model:
            position = rl.Vector3(self.parent.x, self.world_y_offset, self.parent.z)
            rl.draw_model(self.model, position, 1.0, rl.WHITE)

class Game_Chunk:
    def __init__(self, game, x, z, max_height=256):
        self.game = game
        self.x = x
        self.z = z
        self.max_height = max_height
        self.num_subchunks = max_height // 16
        self.subchunks = [SubChunk(self, i) for i in range(self.num_subchunks)]

        # Preenchimento inicial de teste (baseado no seu código original)
        for lx in range(16):
            for lz in range(16):
                for ly in range(max_height):
                    if ly < 2:
                        self.place_block_local(lx, ly, lz, 1) # ID 1 = Grama

    def place_block_local(self, lx, ly, lz, block_id):
        if ly < 0 or ly >= self.max_height: return
        sub_idx = ly // 16
        local_y = ly % 16
        self.subchunks[sub_idx].set_block(lx, local_y, lz, block_id)
        
        # Se colocar um bloco na borda, marca o chunk vizinho como dirty para atualizar as faces
        # (Lógica a ser adicionada na fase de Threads)

    def get_block_global(self, gx, gy, gz):
        """Busca o bloco lidando com coordenadas globais do mundo, atravessando chunks vizinhos se necessário."""
        if gy < 0 or gy >= self.max_height: return 0
        
        if self.x <= gx < self.x + 16 and self.z <= gz < self.z + 16:
            # Está dentro deste chunk
            lx, lz = gx - self.x, gz - self.z
            sub_idx = gy // 16
            local_y = gy % 16
            return self.subchunks[sub_idx].get_block(lx, local_y, lz)
        else:
            # Está em um chunk vizinho
            chunk_x = (gx // 16) * 16
            chunk_z = (gz // 16) * 16
            neighbor = self.game.loaded_chunks.get((chunk_x, chunk_z))
            if neighbor:
                lx, lz = gx - chunk_x, gz - chunk_z
                sub_idx = gy // 16
                local_y = gy % 16
                return neighbor.subchunks[sub_idx].get_block(lx, local_y, lz)
            return 0 # Chunk não carregado

    def update(self, dt):
        # Reconstrói a malha de qualquer subchunk que foi alterado
        for sub in self.subchunks:
            if sub.is_dirty:
                sub.build_mesh()

    def render(self):
        for sub in self.subchunks:
            sub.render()