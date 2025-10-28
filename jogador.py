import time
from pyray import Vector3 
import pyray as rl
import math
from block import Block

class Jogador():

    def __init__(self, game):
        self.game = game
        self.pos = Vector3(0, 2, 0)
        self.dims = Vector3(1, 2, 1)
        self.walk_speed = 0.1
        self.vel = Vector3(0, 0, 0)
        self.on_ground = True
        self.lives = 5
        self.time_invulnerable = 0
        self.forward = Vector3(1,0,0)
        self.right = Vector3(0,0,1)
        self.forca_pulo = 0.4
        self.time_invunerability = 100
        self.lives = 5
        self.f3_active = False
        self.yaw = 0
        self.render_distance = 2
        self.chunck_coord = (int(math.floor(self.pos.x / 16)) * 16, int(math.floor(self.pos.z / 16)) * 16)
        self.last_W_reset = 10
        self.last_W = self.last_W_reset
        self.running = False

        self.time = 0

        # chakra
        self.tempoChakra = 0
        self.elemento = None
        self.posChakra = {"regiao": None,"tempo1": 0, "tempo2": 0, "subregiao": None, "tempo3": 0}
        self.modo = 'mobilidade'
        self.treshold = [0.11, 0.12, 0.11]
        self.treshold = [10, 12, 10]
        self.vezesUsado = {"agua": 0, "fogo": 0, "terra": 0, "vento": 0, "relampago": 0, "chakra": 0}

    def input_chakra(self, tecla):
        # Check pressed keys
        print(tecla)
        match (tecla):
            case 'SHIFT_DOWN':
                self.toggleChakra()

            case 'A_DOWN' | 'S_DOWN' | 'D_DOWN':
                if self.modo == 'chakra' and self.elemento == None:
                    tempoAntes = self.tempoChakra
                    self.tempoChakra = self.time
                    if self.posChakra["regiao"] == None:
                        self.posChakra["regiao"] = tecla[0]
                    else:
                        self.posChakra["subregiao"] = tecla[0]
                        self.posChakra["tempo2"] = self.tempoChakra - tempoAntes

            case 'A_UP' | 'S_UP' | 'D_UP':
                if self.modo == 'chakra' and self.elemento == None:
                    tempoAntes = self.tempoChakra
                    self.tempoChakra = self.time
                    if self.posChakra["subregiao"] == None:
                        self.posChakra["tempo1"] = self.tempoChakra - tempoAntes
                    else:
                        self.posChakra["tempo3"] = self.tempoChakra - tempoAntes
                        if self.elemento == None:
                            self.escolheElemento()

    def input(self,event):
        self.input_chakra(event)

    def update(self,dt):
        self.time +=1
        if rl.is_key_pressed(rl.KEY_F3):
            self.f3_active = not self.f3_active

        if self.time_invulnerable > 0:
            self.time_invulnerable -= 1

        # --- Movimento do jogador ---
        move = Vector3(0, 0, 0)
        if rl.is_key_down(rl.KEY_W):
            if self.last_W <= 0:
                self.last_W = self.last_W_reset
            move.x += self.forward.x
            move.z += self.forward.z
            if self.last_W < self.last_W_reset and self.last_W > 0:
                self.running = True

        else:
            if self.running:
                self.running = False
            self.last_W -= 1
            
        if rl.is_key_down(rl.KEY_S):
            move.x -= self.forward.x
            move.z -= self.forward.z
        if rl.is_key_down(rl.KEY_A):
            move.x += self.right.x
            move.z += self.right.z
        if rl.is_key_down(rl.KEY_D):
            move.x -= self.right.x
            move.z -= self.right.z

        length = math.sqrt(move.x**2 + move.z**2)
        if length:
            move.x /= length
            move.z /= length

        multiplier = 1.5 if self.running else 1.0
        self.vel.x += move.x * self.walk_speed*multiplier
        self.vel.z += move.z * self.walk_speed*multiplier

        # --- Pulo ---
        if rl.is_key_pressed(rl.KEY_SPACE) and self.on_ground:
            self.vel = rl.vector3_add(self.vel, Vector3(0, self.forca_pulo, 0)) 
            self.on_ground = False

        
        self.vel = rl.vector3_subtract(self.vel, Vector3(0, self.game.gravity, 0))
        future_x = self.pos.x + self.vel.x
        if self.game.check_collision_with_blocks(future_x, self.pos.y, self.pos.z, self.dims):
            future_x = self.pos.x
            self.vel.x = 0
        future_y = self.pos.y + self.vel.y
        if self.game.check_collision_with_blocks(self.pos.x, future_y, self.pos.z, self.dims):
            future_y = self.pos.y
            self.on_ground = True
            self.vel.y = 0
        else:
            self.on_ground = False
        future_z = self.pos.z + self.vel.z
        if self.game.check_collision_with_blocks(self.pos.x, self.pos.y, future_z, self.dims):
            future_z = self.pos.z
            self.vel.z = 0
        self.pos = Vector3(future_x, future_y, future_z)
        new_chunck_coord = (int(math.floor(self.pos.x / 16)) * 16, int(math.floor(self.pos.z / 16)) * 16)
        if new_chunck_coord[0] != self.chunck_coord[0] or new_chunck_coord[1] != self.chunck_coord[1]:
            self.game.update_chunk(self.chunck_coord, new_chunck_coord)
        self.chunck_coord = new_chunck_coord
        self.vel = rl.vector3_multiply(self.vel, Vector3(self.game.air_resistance, 1, self.game.air_resistance))

        # --- Colocar bloco ---
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT):
            block_pos = self.game.camera.get_block_looked_at()
            if block_pos:
                print(block_pos)
                bx, by, bz = block_pos
                chunk = self.game.loaded_chunks.get((int(math.floor(bx / 16)) * 16, int(math.floor(bz / 16)) * 16))
                if chunk:
                    local_x = int(bx - chunk.x)
                    local_y = int(by)
                    local_z = int(bz - chunk.z)
                    if chunk.get_block(local_x, local_y, local_z) is None:
                        active_faces = [True, True, True, True, True, True]
                        new_block = Block(chunk, self.game.assets_loader, "grass.png", rl.Vector3(bx, by, bz), active_faces=active_faces)
                        chunk.static_blocks[local_x][local_y][local_z] = new_block
                        chunk.update_adjacent_faces(local_x, local_y, local_z)

    def render(self):
        if (self.time_invulnerable//10) % 2 ==0:
            # Se self.pos representa o canto superior, converte para o centro do cubo
            cube_pos = Vector3(
                self.pos.x,   # mover para o centro em X
                self.pos.y + self.dims.y-1,   # do topo para o centro em Y (baixo -> topo)
                self.pos.z    # mover para o centro em Z
            )
            rl.draw_cube_v(cube_pos, self.dims, rl.BLUE)
            

    def hurt(self):
        if self.time_invulnerable > 0:
            return
        self.time_invulnerable = self.time_invunerability
        self.lives-=1
            
    def render_hud(self):
        for i in range(self.lives):
            x = 20 + i * 35
            y = 20
            rl.draw_rectangle(x, y, 30, 30, rl.RED)

        # invulnerabilidade
        if self.time_invulnerable>0:
            rl.draw_text("INVULNERÁVEL", 20, 60, 25, rl.GOLD)

        rl.draw_text("F5 alterna visão", 10, 100, 20, rl.GRAY)

        self.render_chakra()

        if self.f3_active:
            text = f"Position:\nX: {self.pos.x}\nY: {self.pos.y}\nZ: {self.pos.z} \
                \nLooking at:\nX: {self.game.camera.camera.target.x}\nY: {self.game.camera.camera.target.y}\nZ: {self.game.camera.camera.target.z}\n"
            rl.draw_text(text, 10, 140, 20, (50,50,50,255))

    def escolheElemento(self):
        
        rapido = [self.posChakra["tempo1"]<self.treshold[0], self.posChakra["tempo2"]<self.treshold[1], self.posChakra["tempo3"]<self.treshold[2]]
        print(f"rapido: {rapido}")
        if rapido == [True, True, True]:
            self.elemento = "relampago"
        elif rapido == [True, True, False]:
            self.elemento = "fogo"
        elif rapido == [False, True, True] or rapido == [True, False, True]:
            self.elemento = "vento"
        elif rapido == [True, False, False] or rapido == [False, False, True] or rapido == [False, True, False]:
            self.elemento = "agua"
        elif rapido == [False, False, False]:
            self.elemento = "terra"
        else:
            raise Exception(f"Erro ao escolher elemento: {rapido}")


    def toggleChakra(self):
        if self.modo == 'mobilidade':
            self.modo = 'chakra'
        else:
            print(f"tempo pressionado primeiro: {round(self.posChakra['tempo1'], 3)} tempo entre pressionamentos: {round(self.posChakra['tempo2'],3)} tempo pressionado segundo: {round(self.posChakra['tempo3'],3)}")
            self.posChakra = {"regiao": None,"tempo1": 0, "tempo2": 0, "subregiao": None, "tempo3": 0}
            self.modo = 'mobilidade'
            self.elemento = None


    def render_chakra(self):
        ALPHA = 0.7  # Define alpha value for filled circles
        match self.elemento:
            case "agua":
                corChakra = rl.Color(0, 0, 255, 255)
            case "fogo":
                corChakra = rl.Color(255, 0, 0, 255)
            case "terra":
                corChakra = rl.Color(255, 122, 0, 255)
            case "vento":
                corChakra = rl.Color(0, 255, 0, 255)
            case "relampago":
                corChakra = rl.Color(255, 255, 0, 255)
            case _:
                if self.modo == 'chakra':
                    corChakra = rl.Color(0, 255, 255, 255)
                else:
                    corChakra = rl.Color(255, 255, 255, 255)
        borda = 5
        
        screen_width = rl.get_screen_width()
        screen_height = rl.get_screen_height()

        posRelativa = (0.01, 0.4)
        posRelativa = (posRelativa[0] * screen_width, posRelativa[1] * screen_height)

        if self.modo == 'chakra':
            cor = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.WHITE
        
        # desenha a borda
        rl.draw_rectangle_lines_ex(
            rl.Rectangle(posRelativa[0], posRelativa[1], screen_width*0.2, screen_height*0.55),
            borda, cor
        )

        # cabeca
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        x, y = int(posRelativa[0]*8.5 + screen_width*0.025), int(posRelativa[1]*1.1 + screen_height*0.05)
        w, h = screen_width*0.025, screen_height*0.05
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # cerebro
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == "A":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        x, y = int(posRelativa[0]*9.42 + screen_width*0.016), int(posRelativa[1]*1.115 + screen_height*0.015)
        w, h = screen_width*0.016, screen_height*0.015
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # olhos e ouvidos
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == "S":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        x, y = int(posRelativa[0]*8.5 + screen_width*0.025), int(posRelativa[1]*1.18 + screen_height*0.015)
        w, h = screen_width*0.025, screen_height*0.015
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # boca e nariz
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == "D":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        x, y = int(posRelativa[0]*9.42 + screen_width*0.016), int(posRelativa[1]*1.26 + screen_height*0.015)
        w, h = screen_width*0.016, screen_height*0.015
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # torax
        if self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == "A":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        x, y = int(posRelativa[0]*7.6 + screen_width*0.035), int(posRelativa[1]*1.38 + screen_height*0.05)
        w, h = screen_width*0.035, screen_height*0.05
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # braços
        if self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == "S":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        # braço esquerdo
        x, y = int(posRelativa[0]*4.5 + screen_width*0.01), int(posRelativa[1]*1.41 + screen_height*0.085)
        w, h = screen_width*0.01, screen_height*0.085
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        # braço direito
        x = int(posRelativa[0]*15.5 + screen_width*0.01)
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # maos
        if self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == "D":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        # mão esquerda
        x, y = int(posRelativa[0]*4.6 + screen_width*0.0085), int(posRelativa[1]*1.85 + screen_height*0.0135)
        w, h = screen_width*0.0085, screen_height*0.0135
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        # mão direita
        x = int(posRelativa[0]*15.8 + screen_width*0.0085)
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # abdomen
        if self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == "A":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        x, y = int(posRelativa[0]*7.9 + screen_width*0.0325), int(posRelativa[1]*1.66 + screen_height*0.025)
        w, h = screen_width*0.0325, screen_height*0.025
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # pernas
        if self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == "S":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        # perna esquerda
        x, y = int(posRelativa[0]*7.6 + screen_width*0.01), int(posRelativa[1]*1.8 + screen_height*0.085)
        w, h = screen_width*0.01, screen_height*0.085
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        # perna direita
        x = int(posRelativa[0]*12.6 + screen_width*0.01)
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        
        # pes
        if self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == "D":
            cor = rl.Color(corChakra.r, corChakra.g, corChakra.b, int(255 * ALPHA))
            cor_borda = corChakra
        elif self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == None:
            cor = rl.Color(0, 255, 255, int(255 * ALPHA))
            cor_borda = rl.Color(0, 255, 255, 255)
        else: 
            cor = rl.Color(255, 255, 255, int(255 * ALPHA))
            cor_borda = rl.WHITE
        # pé esquerdo
        x, y = int(posRelativa[0]*5.3 + screen_width*0.0175), int(posRelativa[1]*2.2 + screen_height*0.015)
        w, h = screen_width*0.0175, screen_height*0.015
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)
        # pé direito 
        x = int(posRelativa[0]*13.5 + screen_width*0.0175)
        rl.draw_ellipse(x, y, w, h, cor)
        rl.draw_ellipse_lines(x, y, w, h, cor_borda)



