from data.src.config import *
from data.src.PooPEngine import pygame_rework
from data.src.GUIs import *

import pygame as pyg
from pygame.locals import *
from sys import exit

pgr.create_font('arial',36) # TITLE
pgr.create_font('arial',30) # Buttons
pgr.create_font('arial',22) #TEXTBOX


if __name__ == "__main__":
    mainMenu()