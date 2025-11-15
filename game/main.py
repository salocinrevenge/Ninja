# /// script
# dependencies = [
# "cffi",
# "raylib"
# ]
# ///

from motor import Motor
import asyncio
from assets_loader import Assets_Loader
from block import Block
from bullet import Bullet
from camera import Camera
from controler import Controler
from enemy import Enemy
from game_chunk import Game_Chunk
from game_manager import Game_Manager
from inventario import Inventario
from item import Item
from jogador import Jogador
from spell import Spell
from utils import *


if __name__ == "__main__":
    motor = Motor()
    asyncio.run(motor.run())

    # Set-ExecutionPolicy RemoteSigned -Scope Process
    # .venv\Scripts\activate
    # python main.py

    # .\venv_old\Scripts\activate
    # python old/coracao.py

    # python -m pygbag --template noctx.tmpl --PYBUILD 3.12 --ume_block 0 .
    # pygbag --ume_block 0 --template noctx.tmpl .
    # pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl --git .