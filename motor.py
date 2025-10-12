import time
from game_manager import Game_Manager
import pyray as rl
import asyncio

class Motor():

    def __init__(self) -> None:
        
        self.FPS_PADRAO = 60.0
        self.UPDATE_CAP = 1.0/self.FPS_PADRAO

        rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
        rl.init_window(1000, 700, b"Ninja")
        rl.set_target_fps(60)
        rl.disable_cursor()

        self.game = Game_Manager(self)

    async def run(self):
        self.running = True
        render = False
        firstTime = 0
        lastTime = time.time()  # retorna o tempo atual em segundos
        passedTime = 0
        unprocessedTime = 0
        frameTime = 0
        frames = 0
        self.fps = 0

        while self.running and not rl.window_should_close():
            render = False
            firstTime = time.time()
            passedTime = firstTime - lastTime   # tempo que passou desde a ultima vez que o loop foi executado
            lastTime = firstTime            # atualiza o tempo da ultima vez que o loop foi executado

            unprocessedTime += passedTime  # tempo nao processado
            frameTime += passedTime

            # enquanto nao processou td q deveria (devido a lag em render ou coisas assim)
            i = 0
            while unprocessedTime >= self.UPDATE_CAP:
                # Isso garante que o tempo de atualizacao seja constante
                # e nao dependa do tempo de renderizacao. Igualando o 
                # jogo para todos os computadores, apenas aumentando o
                # fps para computadores mais potentes
                unprocessedTime -= self.UPDATE_CAP  # Tempo comido
                render = True

                self.update(self.UPDATE_CAP)

                if frameTime >= 1.0:
                        frameTime = 0
                        self.fps = frames
                        frames = 0
                        # print("FPS: " + str(fps))
                i +=1
                if i >1: # apenas 2 repeticoes no maximo
                     break

            # Depois de processar o tempo, renderiza
            if render:
                self.render()
                frames += 1
            # else:
            #     time.sleep(0.001)
                
            await asyncio.sleep(0)
                
        self.dispose()
      
    def update(self, dt): # metodo chamado a cada frame
        self.game.update(dt)

    def render(self): # metodo chamado a cada frame

        # Renderizar o mapa
        self.game.render()
        # mostra o FPS no canto superior direito
        rl.draw_text(f"FPS: {self.fps}", rl.get_screen_width() - 100, 10, 20, rl.RED)


    def dispose(self):      # metodo chamado quando o jogo fecha
            pass
