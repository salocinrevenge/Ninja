import time
from pyray import Vector3 
import pyray as rl
import math
from block import Block
from utils import check_colision_point
from inventario import Inventario
from spell import Spell
import copy

class Jogador():

    def __init__(self, game):
        self.game = game
        self.pos = Vector3(0, 2, 0)
        self.dims = Vector3(0.8, 1.9, 0.8)
        self.walk_speed = 0.1
        self.vel = Vector3(0, 0, 0)
        self.on_ground = True
        self.lives = 5
        self.time_invulnerable = 0
        self.forward = Vector3(1,0,0)
        self.right = Vector3(0,0,1)
        self.forca_pulo = 0.4
        self.time_invulnerability = 100
        self.lives = 5
        self.f1_active = False
        self.f3_active = False
        self.yaw = 0
        self.render_distance = 2
        self.chunck_coord = (int(math.floor(self.pos.x / 16)) * 16, int(math.floor(self.pos.z / 16)) * 16)
        self.last_W_reset = 10
        self.last_W = self.last_W_reset
        self.running = False
        self.third_person = False
        self.eye_height = 1.75
        self.can_place_block = True
        self.can_break_block = True
        self.time = 0
        self.time_message = 0
        self.messages = []
        self.inventario = Inventario(jogador=self)

        self.pressed_move_keys = {"W":False, "A":False, "S":False, "D":False}

        # chakra
        self.tempoChakra = 0
        self.elemento = None
        self.posChakra = {"regiao": None,"tempo1": 0, "tempo2": 0, "subregiao": None, "tempo3": 0}
        self.modo = 'mobilidade'
        self.treshold = [0.11, 0.12, 0.11]
        self.treshold = [10, 12, 10]
        self.vezesUsado = {"agua": 0, "fogo": 0, "terra": 0, "ar": 0, "relampago": 0, "chakra": 0}
        self.jumping = False
        self.pilha_conjuracao = []

    

    def input_chakra(self, tecla):
        match (tecla):
            case 'SHIFT_DOWN':
                self.toggleChakra()

            case 'A_DOWN' | 'S_DOWN' | 'D_DOWN':
                if self.elemento != None:
                    self.elemento = None
                    self.posChakra = {"regiao": None,"tempo1": 0, "tempo2": 0, "subregiao": None, "tempo3": 0}
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

    def try_place_block(self):
        block_pos = self.game.camera.get_block_looked_at()
        if block_pos:
            bx, by, bz, face = block_pos
            by += {"top": 1, "bottom": -1}.get(face, 0)
            bz += {"north": 1, "south": -1}.get(face, 0)
            bx += {"east": 1, "west": -1}.get(face, 0)
            chunk = self.game.loaded_chunks.get((int(math.floor(bx / 16)) * 16, int(math.floor(bz / 16)) * 16))
            if chunk:
                local_x = int(bx - chunk.x)
                local_y = int(by)
                local_z = int(bz - chunk.z)
                if chunk.get_block(local_x, local_y, local_z) is None and not check_colision_point(self.pos, self.dims, Vector3(bx, by, bz), Vector3(1,1,1)):
                    active_faces = [True, True, True, True, True, True]
                    new_block = Block(chunk, self.game.assets_loader, "grass.png", rl.Vector3(bx, by, bz), active_faces=active_faces)
                    ok = chunk.place_block(local_x, local_y, local_z, new_block)
                    if ok is not None:
                        self.messages.append((ok, 120))


    def try_break_block(self):
        block_pos = self.game.camera.get_block_looked_at()
        if block_pos:
            bx, by, bz, face = block_pos
            chunk = self.game.loaded_chunks.get((int(math.floor(bx / 16)) * 16, int(math.floor(bz / 16)) * 16))
            if chunk:
                local_x = int(bx - chunk.x)
                local_y = int(by)
                local_z = int(bz - chunk.z)
                bloco = chunk.get_block(local_x, local_y, local_z)
                if bloco is not None:
                    chunk.remove_block(local_x, local_y, local_z)

    def input(self,event):
        self.inventario.input(event)
        self.input_chakra(event)
        match event:
            case 'F1_DOWN':
                self.f1_active = not self.f1_active
            case 'F3_DOWN':
                self.f3_active = not self.f3_active
            case 'F5_DOWN':
                self.third_person = not self.third_person
            case 'SPACE_DOWN':
                if self.on_ground:
                    self.jumping = True
            case 'SPACE_UP':
                self.jumping = False
            case 'RIGHT_MOUSE_DOWN':
                if self.modo == 'chakra':
                    if self.posChakra['regiao'] != None:
                        spell = Spell(caster=self, body=self.posChakra['regiao'], subbody=self.posChakra['subregiao'], element= self.elemento)
                        self.pilha_conjuracao.append(spell)
                        self.elemento = None
                        self.posChakra = {"regiao": None,"tempo1": 0, "tempo2": 0, "subregiao": None, "tempo3": 0}
                    else:
                        hp = self.inventario.get_selected_hand_position()
                        if hp is not None:
                            self.pilha_conjuracao.append(Spell(caster=self,hand_position=hp))
                    print(f"Pilha de conjuracao: {self.pilha_conjuracao}")
                elif self.modo == 'mobilidade' and self.can_place_block:
                    self.try_place_block()
                    self.can_place_block = False
            case 'RIGHT_MOUSE_UP':
                self.can_place_block = True
            case 'LEFT_MOUSE_DOWN':
                if self.modo == 'chakra':
                    self.activate_spell()
                elif self.modo == 'mobilidade' and self.can_break_block:
                    self.try_break_block()
                    self.can_break_block = False
            case 'LEFT_MOUSE_UP':
                self.can_break_block = True
            case 'A_DOWN' | 'S_DOWN' | 'D_DOWN' | 'W_DOWN':
                if self.modo == 'mobilidade' or event == 'W_DOWN':
                    self.pressed_move_keys[event.split('_')[0]] = True
            case 'A_UP' | 'S_UP' | 'D_UP' | 'W_UP':
                if self.modo == 'mobilidade' or event == 'W_UP':
                    self.pressed_move_keys[event.split('_')[0]] = False

    def activate_spell(self):
        if len(self.pilha_conjuracao) ==0:
            return
        spell = self.pilha_conjuracao.pop()
        if spell.element:
            self.cast_spell(spell)
            return
        if len(self.pilha_conjuracao) ==0:
            return
        if spell.hand_position == "double":
            if self.pilha_conjuracao[-1].element:
                for _ in range(spell.properties["multipling"] -1):
                    self.pilha_conjuracao.append(copy.copy(self.pilha_conjuracao[-1]))
                return
            if self.pilha_conjuracao[-1].hand_position:
                self.pilha_conjuracao[-1].double_all_properties()
                return
            return
        self.pilha_conjuracao[-1].merge(spell)
        self.activate_spell()


    def cast_spell(self, spell):
        print(f"Conjurando {spell}!")

    def movement(self):
        if self.jumping and self.on_ground:
            self.vel = rl.vector3_add(self.vel, Vector3(0, self.forca_pulo, 0)) 
            self.on_ground = False

        move = Vector3(0, 0, 0)
        if self.pressed_move_keys["W"]:
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

        if self.pressed_move_keys["S"]:
            move.x -= self.forward.x
            move.z -= self.forward.z
        if self.pressed_move_keys["A"]:
            move.x += self.right.x
            move.z += self.right.z
        if self.pressed_move_keys["D"]:
            move.x -= self.right.x
            move.z -= self.right.z

        length = math.sqrt(move.x**2 + move.z**2)
        if length:
            move.x /= length
            move.z /= length

        multiplier = 1.5 if self.running else 1.0
        self.vel.x += move.x * self.walk_speed*multiplier
        self.vel.z += move.z * self.walk_speed*multiplier


        
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

    def update(self,dt):
        self.inventario.update(dt)
        self.time +=1
        if self.time_message >0:
            self.time_message -=1
            if self.time_message ==0:
                if len(self.messages)>0:
                    self.messages.pop(0)
        else:
            if len(self.messages)>0:
                self.message = self.messages[0][0]
                self.time_message = self.messages[0][1]
        if self.time_invulnerable > 0:
            self.time_invulnerable -= 1
        self.movement()            

    def render(self):
        if (self.time_invulnerable//10) % 2 ==0:
            # Se self.pos representa o canto superior, converte para o centro do cubo
            cube_pos = Vector3(
                self.pos.x,   # mover para o centro em X
                self.pos.y + self.dims.y-1,   # do topo para o centro em Y (baixo -> topo)
                self.pos.z    # mover para o centro em Z
            )
            if self.third_person:
                rl.draw_cube_v(cube_pos, self.dims, rl.BLUE)

    def hurt(self):
        if self.time_invulnerable > 0:
            return
        self.time_invulnerable = self.time_invunerability
        self.lives-=1
            
    def show_message(self):
        if self.time_message >0 and len(self.messages)>0:
            font_size = 32
            # Calculate text width to center it
            text_width = rl.measure_text(self.messages[0][0], font_size)
            x = rl.get_screen_width()//2 - text_width//2
            y = rl.get_screen_height() - 250
            # Draw black border by offsetting text
            rl.draw_text(self.messages[0][0], x-1, y-1, font_size, rl.BLACK)
            rl.draw_text(self.messages[0][0], x+1, y-1, font_size, rl.BLACK) 
            rl.draw_text(self.messages[0][0], x-1, y+1, font_size, rl.BLACK)
            rl.draw_text(self.messages[0][0], x+1, y+1, font_size, rl.BLACK)
            # Draw main red text
            rl.draw_text(self.messages[0][0], x, y, font_size, rl.RED)

    def render_hud(self):
        if self.f1_active:
            return
        
        
        for i in range(self.lives):
            x = 20 + i * 35
            y = 20
            rl.draw_rectangle(x, y, 30, 30, rl.RED)

        # invulnerabilidade
        if self.time_invulnerable>0:
            rl.draw_text("INVULNERÁVEL", 20, 60, 25, rl.GOLD)

        if self.modo == 'chakra' or self.f3_active:
            self.render_chakra()
        if len(self.pilha_conjuracao) > 0 or self.f3_active or self.modo == 'chakra':
            self.render_spell_stack()

        self.inventario.render()
        # Draw crosshair
        screen_width = rl.get_screen_width()
        screen_height = rl.get_screen_height()
        center_x = screen_width // 2 
        center_y = screen_height // 2
        size = 10
        # Draw black border lines first
        # Draw multiple black lines to create a thicker border
        for offset in [-1, 0, 1]:
            rl.draw_line(center_x - size - 1, center_y + offset, center_x + size + 1, center_y + offset, rl.BLACK)
            rl.draw_line(center_x + offset, center_y - size - 1, center_x + offset, center_y + size + 1, rl.BLACK)
        # Draw white crosshair on top
        rl.draw_line(center_x - size, center_y, center_x + size, center_y, rl.WHITE)
        rl.draw_line(center_x, center_y - size, center_x, center_y + size, rl.WHITE)

        if self.f3_active:
            text = f"Position:\nX: {self.pos.x}\nY: {self.pos.y}\nZ: {self.pos.z} \
                \nLooking at:\nX: {self.game.camera.camera.target.x}\nY: {self.game.camera.camera.target.y}\nZ: {self.game.camera.camera.target.z}\n"
            rl.draw_text(text, 10, 100, 20, (50,50,50,255))

            # mostra o FPS no canto superior direito
            rl.draw_text(f"FPS: {self.game.motor.fps}", rl.get_screen_width() - 100, 10, 20, rl.RED)

        self.show_message()
        
    def escolheElemento(self):
        rapido = [self.posChakra["tempo1"]<self.treshold[0], self.posChakra["tempo2"]<self.treshold[1], self.posChakra["tempo3"]<self.treshold[2]]
        if self.f3_active:
            print(f"rapido: {rapido}")
        if rapido == [True, True, True]:
            self.elemento = "relampago"
        elif rapido == [True, True, False]:
            self.elemento = "fogo"
        elif rapido == [False, True, True] or rapido == [True, False, True]:
            self.elemento = "ar"
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
            if self.f3_active:
                print(f"tempo pressionado primeiro: {round(self.posChakra['tempo1'], 3)} tempo entre pressionamentos: {round(self.posChakra['tempo2'],3)} tempo pressionado segundo: {round(self.posChakra['tempo3'],3)}")
            self.posChakra = {"regiao": None,"tempo1": 0, "tempo2": 0, "subregiao": None, "tempo3": 0}
            self.modo = 'mobilidade'
            self.elemento = None

    def render_chakra(self):
        ALPHA = 0.7  # Define alpha value for filled circles
        ok,corChakra = self.game.assets_loader.color_element(self.elemento)
        corChakra = rl.Color(*corChakra)
        if not ok:
            if self.modo == 'chakra':
                corChakra = rl.Color(0, 255, 255, 255)
                
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

    def render_spell_stack(self):
        # Constants for the spell display
        SPELL_SIZE = 40
        PADDING = 5
        BORDER = 2
        MAX_WIDTH = rl.get_screen_width() // 3  # Use 1/3 of screen width
        
        if not self.pilha_conjuracao:  # If stack is empty, don't draw anything
            return
            
        # Calculate total width needed
        total_spells = len(self.pilha_conjuracao)
        total_width = (SPELL_SIZE + PADDING) * total_spells - PADDING
        
        # Calculate how many spells we can show
        spells_that_fit = min(total_spells, MAX_WIDTH // (SPELL_SIZE + PADDING))
        actual_width = (SPELL_SIZE + PADDING) * spells_that_fit - PADDING
        
        # Calculate starting position (centered horizontally, above inventory)
        start_x = (rl.get_screen_width() - actual_width) // 2
        start_y = rl.get_screen_height() - 150  # Above inventory
        
        # Draw background rectangle
        rl.draw_rectangle(start_x - PADDING, start_y - PADDING, 
                 actual_width + PADDING * 2, SPELL_SIZE + PADDING * 2, 
                 rl.Color(40, 40, 40, self.inventario.alpha_hotbar))
        
        # Draw spells from right to left (newest first)
        start_index = max(0, total_spells - spells_that_fit)
        for i, spell in enumerate(self.pilha_conjuracao[start_index:]):
            x = start_x + i * (SPELL_SIZE + PADDING)
            spell.render_rune(x,start_y,SPELL_SIZE)
            rl.draw_rectangle_lines_ex(rl.Rectangle(x, start_y, SPELL_SIZE, SPELL_SIZE),BORDER, rl.WHITE)



