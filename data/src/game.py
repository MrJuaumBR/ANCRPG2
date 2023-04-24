import pygame as pyg
from pygame.locals import *
from .Player import Player
from .groups import *

def game(pgr,Connection,MyStyle):
    run = True
    collideGroup =CollideGroup(pgr)
    cameraGroup = CameraGroup(pgr)
    plr = Player((collideGroup,cameraGroup),pgr,(0,0),(64,64))
    while run:
        for ev in pyg.event.get():
            if ev.type == QUIT:
                pyg.quit()
                run = False

        cameraGroup.custom_draw(plr)
        plr.update()
        pgr.update()
        pgr.fill()