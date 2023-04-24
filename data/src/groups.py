import pygame as pyg
from pygame.locals import *

class CollideGroup(pyg.sprite.Group):
    def __init__(self,pgr):
        super().__init__()
        pyg.init()

        self.pgr = pgr
        self.window = self.pgr.window

class CameraGroup(pyg.sprite.Group):
    def __init__(self,pgr):
        super().__init__()
        pyg.init()

        self.pgr = pgr
        self.display_surface = pyg.display.get_surface()
        self.structures = []

        # Camera OffSet
        self.offset = pyg.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Zoom
        self.zoom_scale = 1
        self.internal_surface_size = (2500,2500)
        self.internal_surface = pyg.Surface(self.internal_surface_size,pyg.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center=(self.half_w,self.half_h))
        self.internal_surface_size_vector = pyg.math.Vector2(self.internal_surface_size)

        # Zoom Offset
        self.internal_offset = pyg.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0]//2-self.half_w
        self.internal_offset.y = self.internal_surface_size[1]//2-self.half_h

    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def zoom_keyboard_control(self):
        keys = pyg.key.get_pressed()
        if (keys[K_i] or keys[K_PLUS] or keys[K_KP_PLUS]) and self.zoom_scale < 1:
            self.zoom_scale += 0.1
        elif (keys[K_o] or keys[K_MINUS] or keys[K_KP_MINUS]) and self.zoom_scale > .1:
            self.zoom_scale -= 0.1

    def custom_draw(self,player):
        self.zoom_keyboard_control()
        self.internal_surface.fill((100,200,200))

        for sprite in sorted(self.sprites() + self.structures,key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset+self.internal_offset
            sprite.draw(self.internal_surface)

        scaled_surface = pyg.transform.scale(self.internal_surface,self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(center = (self.half_w,self.half_h))

        self.center_target_camera(player)