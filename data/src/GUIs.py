from .PooPEngine import pygame_rework, Server
from .config import *

import pygame as pyg
from pygame.locals import *
from sys import exit
import sqlite3 as sql
import socket

pyg.init()
pgr = pygame_rework(GAME_SCREEN_SIZE,GAME_TITLE)
pgr.create_window()

def multiplayerMode():
    run = True
    player_nick = ""
    textbox_player_nick = False
    MYIPV4 = socket.gethostbyname(socket.gethostname())
    IPV4_HOST = ""
    while run:
        backbtn = pgr.button((75,15),((0,0,0),(200,100,100)),"BACK",1)
        pgr.text((pgr.hScrSize[0],pgr.hScrSize[1]-275),(0,0,0),"Player Nick:",0)
        textbox_player_nick,player_nick = pgr.textbox((pgr.hScrSize[0],pgr.hScrSize[1]-250,150,20),((100,100,100),(00,0,0),(200,200,200)),2,textbox_player_nick,player_nick)
        pyg.draw.line(pgr.window,(0,0,0),(0,pgr.hScrSize[1]+175),(pgr.scrSize[0],pgr.hScrSize[1]+175))
        # Host
        hostgameBtn = pgr.button((pgr.hScrSize[0],pgr.hScrSize[1]+225),((0,0,0),(100,100,100)),"Host Game",2)
        copyHostBtn = pgr.button((pgr.hScrSize[0]+225,pgr.hScrSize[1]+225),((0,0,0),(100,100,100)),f"Click to copy: {MYIPV4}",2)

        # join
        entergameBtn = pgr.button((pgr.hScrSize[0],pgr.hScrSize[1]+275),((0,0,0),(100,100,100)),"Enter Game",2)
        pasteHostBtn = pgr.button((pgr.hScrSize[0]+225,pgr.hScrSize[1]+275), ((0,0,0),(100,100,100)), f"Paste Host: {IPV4_HOST}",2)

        if pasteHostBtn:
            IPV4_HOST= pgr.pasteFromClipboard()
        if copyHostBtn:
            pgr.copyToClipboard(socket.gethostbyname(socket.gethostname()))
        if hostgameBtn:
            from .game import game
            game(pgr,IPV4_HOST,"Host")
        if backbtn:
            run = False
        for ev in pgr.events():
            if ev.type ==QUIT:
                pyg.quit()
                exit()
            if pgr.key_pressed(ev,K_ESCAPE):
                run = False

        pgr.update()
        pgr.fill()

def characterSelect():
    run = True
    while run:
        pyg.draw.line(pgr.window,(0,0,0),(0,pgr.hScrSize[1]+175),(pgr.scrSize[0],pgr.hScrSize[1]+175))
        singleplayerBtn = pgr.button((pgr.hScrSize[0]-150,pgr.hScrSize[1]+250),((0,0,0),(200,200,200)),"SINGLE",1)
        multiplayerBtn = pgr.button((pgr.hScrSize[0]+150,pgr.hScrSize[1]+250),((0,0,0),(200,200,200)),"MULTIPLAYER",1)
        backbtn = pgr.button((75,15),((0,0,0),(200,100,100)),"BACK",1)
        if backbtn:
            run = False
        if multiplayerBtn:
            multiplayerMode()
        for ev in pgr.events():
            if ev.type ==QUIT:
                pyg.quit()
                exit()
            if pgr.key_pressed(ev,K_ESCAPE):
                run = False

        pgr.update()
        pgr.fill()


def mainMenu():
    pgr.database = sql.connect('./data/savedata.db')
    pgr.cursor = pgr.database.cursor()
    while True:
        pgr.text((pgr.hScrSize[0],pgr.hScrSize[1]-250),(0,0,0),GAME_TITLE,0)
        playBtn = pgr.button((pgr.hScrSize[0],pgr.hScrSize[1]-150),((0,0,0),(200,200,200)),"PLAY",1)
        if playBtn:
            characterSelect()
        optionBtn = pgr.button((pgr.hScrSize[0],pgr.hScrSize[1]-100),((0,0,0),(200,200,200)),"OPTIONS",1)
        exitBtn = pgr.button((pgr.hScrSize[0],pgr.hScrSize[1]-50),((0,0,0),(200,100,100)),"EXIT",1)
        for ev in pgr.events():
            if ev.type == QUIT:
                pyg.quit()
                exit()

        pgr.update()
        pgr.fill()