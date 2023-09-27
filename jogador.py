import time
import pygame

class Jogador():
    def __init__(self):
        self.tempoChakra = 0
        self.elemento = None
        self.posChakra = {"regiao": None,"tempo1": 0, "tempo2": 0, "subregiao": None, "tempo3": 0}
        self.modo = 'mobilidade'
        self.treshold = [0.11, 0.12, 0.11]
        vezesUsado = {"agua": 0, "fogo": 0, "terra": 0, "vento": 0, "relampago": 0, "chakra": 0}

    def tick(self):
        pass

    def renderGUI(self, screen):
        match self.elemento:
            case "agua":
                corChakra = (0,0,255)
            case "fogo":
                corChakra = (255,0,0)
            case "terra":
                corChakra = (255,122,0)
            case "vento":
                corChakra = (0,255,0)
            case "relampago":
                corChakra = (255,255,0)
            case _:
                if self.modo == 'chakra':
                    corChakra = (0,255,255)
                else:
                    corChakra = (255,255,255)
        borda = 5
        #recebe as dimensoes da tela
        screen_width, screen_height = screen.get_size()

        posRelativa = (0.01,0.4)# 0 a 1 da tela em ambas direcoes
        posRelativa = (posRelativa[0]*screen_width, posRelativa[1]*screen_height)

        if self.modo == 'chakra':
            cor = (0,255,255)
        else: cor = (255,255,255)
        # desenha a borda
        pygame.draw.rect(screen, cor, (posRelativa[0],posRelativa[1],screen_width*0.2,screen_height*0.55), width=borda, border_radius=10)

        # cabeca
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*8.5, posRelativa[1]*1.1, screen_width*0.05, screen_height*0.1), width=borda)
        
        # cerebro
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == "A":
            cor = corChakra
        elif self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*9.42, posRelativa[1]*1.115, screen_width*0.032, screen_height*0.03), width=borda)
        

        # olhos e ouvidos
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == "S":
            cor = corChakra
        elif self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*8.5, posRelativa[1]*1.18, screen_width*0.05, screen_height*0.03), width=borda)
        
        # boca e nariz
        if self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == "D":
            cor = corChakra
        elif self.posChakra["regiao"] == "A" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*9.42, posRelativa[1]*1.26, screen_width*0.032, screen_height*0.03), width=borda)
        

        
        # torax
        if self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == "A":
            cor = corChakra
        elif self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*7.6, posRelativa[1]*1.38, screen_width*0.07, screen_height*0.1), width=borda)
        
        # braços
        if self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == "S":
            cor = corChakra
        elif self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*4.5, posRelativa[1]*1.41, screen_width*0.02, screen_height*0.17), width=borda)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*15.5, posRelativa[1]*1.41, screen_width*0.02, screen_height*0.17), width=borda)
        
        # maos
        if self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == "D":
            cor = corChakra
        elif self.posChakra["regiao"] == "S" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*4.6, posRelativa[1]*1.85, screen_width*0.017, screen_height*0.027), width=borda)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*15.8, posRelativa[1]*1.85, screen_width*0.017, screen_height*0.027), width=borda)
        

        # abdomen
        if self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == "A":
            cor = corChakra
        elif self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*7.9, posRelativa[1]*1.66, screen_width*0.065, screen_height*0.05), width=borda)
        
        # pernas
        if self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == "S":
            cor = corChakra
        elif self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*7.6, posRelativa[1]*1.8, screen_width*0.02, screen_height*0.17), width=borda)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*12.6, posRelativa[1]*1.8, screen_width*0.02, screen_height*0.17), width=borda)
        
        # pes
        if self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == "D":
            cor = corChakra
        elif self.posChakra["regiao"] == "D" and self.posChakra["subregiao"] == None:
            cor = (0,255,255)
        else: cor = (255,255,255)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*5.3, posRelativa[1]*2.2, screen_width*0.035, screen_height*0.03), width=borda)
        pygame.draw.ellipse(screen, cor, (posRelativa[0]*13.5, posRelativa[1]*2.2, screen_width*0.035, screen_height*0.03), width=borda)


    def renderBody(self, screen):
        # renderiza a cabeca
        posInicial = (800,200)
        pygame.draw.ellipse(screen, (255,0,0), (posInicial[0]+0,posInicial[1]+0,90,100) )

        vertices  = [(37,120), (37,110), (52,110), (52,120), (83,124), (100,131)]
        for i in range(len(vertices)):
            vertices[i]= (vertices[i][0]+posInicial[0], vertices[i][1]+posInicial[1])
        pygame.draw.polygon(screen, (255,0,0), vertices)

    def render(self, screen):
        self.renderGUI(screen)
        self.renderBody(screen)
        pass

    def escolheElemento(self):
        
        rapido = [self.posChakra["tempo1"]<self.treshold[0], self.posChakra["tempo2"]<self.treshold[1], self.posChakra["tempo3"]<self.treshold[2]]
        
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
            

    def input(self, tecla):

        match (tecla):

            case 'SHIFT':
                self.toggleChakra()

            case 'A' | 'S' | 'D':
                if self.modo == 'chakra':
                    tempoAntes = self.tempoChakra
                    self.tempoChakra = time.time()
                    if self.posChakra["regiao"] == None:
                        self.posChakra["regiao"] = tecla
                    else:
                        self.posChakra["subregiao"] = tecla
                        self.posChakra["tempo2"] = self.tempoChakra - tempoAntes

            case 'a' | 's' | 'd':
                if self.modo == 'chakra':
                    tempoAntes = self.tempoChakra
                    self.tempoChakra = time.time()
                    if self.posChakra["subregiao"] == None:
                        self.posChakra["tempo1"] = self.tempoChakra - tempoAntes
                    else:
                        self.posChakra["tempo3"] = self.tempoChakra - tempoAntes
                        if self.elemento == None:
                            self.escolheElemento()

 