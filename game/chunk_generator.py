import multiprocessing as mp

def chunk_worker(request_queue, result_queue, max_height):
    """
    Função que roda em núcleos separados do processador.
    Não coloque NENHUMA função do Raylib aqui dentro (rl.algo).
    """
    while True:
        try:
            task = request_queue.get()
            if task is None:
                break # Sinal para fechar o processo
            
            chunk_x, chunk_z = task
            num_subchunks = max_height // 16
            
            # chunk_data será uma lista de subchunks.
            # Cada subchunk é um array 1D de 4096 blocos (16x16x16)
            chunk_data = []

            for sub_idx in range(num_subchunks):
                world_y_offset = sub_idx * 16
                blocks = [0] * (16 * 16 * 16) # Ar
                
                # Geração de terreno provisória (tudo abaixo de Y=2 é grama/ID=1)
                for ly in range(16):
                    gy = world_y_offset + ly
                    if gy < 2:
                        for lx in range(16):
                            for lz in range(16):
                                blocks[lx + lz * 16 + ly * 256] = 1
                
                chunk_data.append(blocks)

            # Devolve a tupla com as coordenadas e os dados prontos
            result_queue.put(((chunk_x, chunk_z), chunk_data))
        except Exception as e:
            print(f"Erro no processamento do chunk: {e}")

class ChunkGenerator:
    def __init__(self, max_height):
        self.request_queue = mp.Queue()
        self.result_queue = mp.Queue()
        self.max_height = max_height
        
        # Deixa 1 núcleo livre para o Raylib (Thread Principal) e 1 para o SO
        self.num_workers = max(1, mp.cpu_count() - 2) 
        self.workers = []

        for _ in range(self.num_workers):
            p = mp.Process(target=chunk_worker, args=(self.request_queue, self.result_queue, self.max_height))
            p.daemon = True
            p.start()
            self.workers.append(p)

    def request_chunk(self, x, z):
        self.request_queue.put((x, z))

    def get_ready_chunks(self):
        """Puxa todos os chunks que os processos já terminaram de calcular"""
        ready = []
        while not self.result_queue.empty():
            ready.append(self.result_queue.get())
        return ready

    def dispose(self):
        for _ in self.workers:
            self.request_queue.put(None)