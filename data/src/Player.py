import pygame as pyg
from pygame.locals import *


class Player(pyg.sprite.Sprite):
    def __init__(self,group,PooPEngine,XY,Size):
        super().__init__(group)
        self.pgr = PooPEngine
        self.Pos = XY   
        self.Size = Size

        self.rect = Rect(self.Pos[0],self.Pos[1],Size[0],Size[1])
        self.color = (0,0,0)
        self.image = None
        self.my_Number = 0

        self.window = self.pgr.window
        self.states = ["live","dead",'menu']
        self.state = 0
        self.velocity = 3
        self.stats = {
            "level":1,
            "points":3,
            "atk":1,
            "def":1,
            "agi":1,
            "qi":1,
            "health":100,
            "maxhealth":100
        }
    def takeDamage(self,damage):
        if self.stats['health'] >= damage:
            self.stats['health'] -= damage
        if self.stats['health'] <= 0:
            self.state = self.states.index('dead')
    
    def healDamage(self,heal):
        if self.stats['health'] >= 1:
            self.stats['health'] += heal

    def draw(self,win):
        if self.image:
            return
        else:
            pyg.draw.rect(win,self.color,self.rect)
        pass
    
    def move(self):
        keys = pyg.key.get_pressed()
        if not self.states[self.state] in ["dead",'menu']:
            if keys[K_d]:
                self.rect.x += self.velocity
            if keys[K_a]:
                self.rect.x -= self.velocity 
            if keys[K_s]:
                self.rect.y += self.velocity
            if keys[K_w]:
                self.rect.y -= self.velocity
        pass

    def update(self):
        self.move()
        pass