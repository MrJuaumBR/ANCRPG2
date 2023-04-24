
from config import *
from Player import Player


class Control():
    def __init__(self):
        self.MaxPlayers = GAME_MULTIPLAYER_MAXPLAYERS
        self.ConnectTo = ""
        self.PlayerClass = Player()