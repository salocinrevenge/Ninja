from block import Block
import pyray as rl

class Game_Chunk():
    def __init__(self,game,x,z,max_height):
        assert x%16 ==0, "x não é múltiplo de 16"
        assert z%16 ==0, "z não é múltiplo de 16"
        self.game = game
        self.x = x
        self.z = z
        self.limits = (16,max_height,16)
        self.static_blocks = []
        for x in range(self.limits[0]):
            self.static_blocks.append([])
            for y in range(self.limits[1]):
                self.static_blocks[-1].append([])
                for z in range(self.limits[2]):
                    bloco = None
                    if y < 2:
                        active_faces = [True, True, True, True, True, True]
                        bloco = Block(self, self.game.assets_loader, "grass", rl.Vector3(x+self.x,y,z+self.z), active_faces=active_faces)
                        # bloco = None
                    self.static_blocks[-1][-1].append(bloco)
                    self.update_adjacent_faces(x,y,z)

    def place_block(self, x, y, z, block):
        if y < 0:
            return
        if y >= self.limits[1]:
            return "Impossible to place block above chunk height of {}".format(self.limits[1])
        self.static_blocks[x][y][z] = block
        self.update_adjacent_faces(x, y, z)

    def remove_block(self, x, y, z):
        self.static_blocks[x][y][z] = None
        self.update_adjacent_faces(x, y, z)

    def update_adjacent_faces(self,x,y,z):
        block = self.get_block(x,y,z)
        # print("Atualizando faces adjacentes de bloco em",x,y,z)
        # Frente (z+1)
        neighbor = self.get_block(x,y,z+1)
        if neighbor:
            if block:
                block.update_face(0,False)
            neighbor.update_face(1,block is None) 
        # Trás (z-1)
        neighbor = self.get_block(x,y,z-1)
        if neighbor:
            if block:
                block.update_face(1,False)
            neighbor.update_face(0,block is None)
        # Direita (x+1)
        neighbor = self.get_block(x+1,y,z)
        if neighbor:
            if block:
                block.update_face(2,False)
            neighbor.update_face(3,block is None)
        # Esquerda (x-1)
        neighbor = self.get_block(x-1,y,z)
        if neighbor:
            if block:
                block.update_face(3,False)
            neighbor.update_face(2,block is None)
        # Topo (y+1)
        neighbor = self.get_block(x,y+1,z)
        if neighbor:
            if block:
                block.update_face(4,False)
            neighbor.update_face(5,block is None)
        # Base (y-1)
        neighbor = self.get_block(x,y-1,z)
        if neighbor:
            if block:
                block.update_face(5,False)
            neighbor.update_face(4,block is None)

    def get_block(self,x,y,z):
        get_from_other_chunk = False
        if x < 0 or x >= len(self.static_blocks):
            get_from_other_chunk = True
        elif y < 0 or y >= len(self.static_blocks[x]):
            return None
        elif z < 0 or z >= len(self.static_blocks[x][y]):
            get_from_other_chunk = True
        if get_from_other_chunk:
            global_x = x + self.x
            global_y = y
            global_z = z + self.z
            chunk_x = (global_x // 16) * 16
            chunk_z = (global_z // 16) * 16
            neighbor_chunk = self.game.loaded_chunks.get((chunk_x, chunk_z))
            if not neighbor_chunk:
                return None
            local_x = global_x - chunk_x
            local_y = global_y
            local_z = global_z - chunk_z
            return neighbor_chunk.get_block(local_x, local_y, local_z)
        else:
        
            return self.static_blocks[x][y][z]

    def render(self):
        for x in range(self.limits[0]):
            for y in range(self.limits[1]):
                for z in range(self.limits[2]):
                    if self.static_blocks[x][y][z]:
                        self.static_blocks[x][y][z].render()

    def update(self, dt):
        pass