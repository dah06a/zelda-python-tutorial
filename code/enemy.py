from tkinter import E
import pygame
from entity import Entity
from settings import *
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups):
        # General setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.status = 'idle'

        # Graphics setup
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

    def import_graphics(self, name):
        self.animations = { 'idle': [], 'move': [], 'attack': [] }
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)