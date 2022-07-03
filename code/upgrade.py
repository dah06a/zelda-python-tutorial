import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_num = len(self.player.stats)
        self.attribute_names = list(self.player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Item creation
        self.width = self.display_surface.get_size()[0] // 6
        self.height = self.display_surface.get_size()[1] * 0.8
        self.create_items()

        # Selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT]:
                if self.selection_index == self.attribute_num - 1:
                    self.selection_index = 0
                else: self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT]:
                if self.selection_index == 0:
                    self.selection_index = self.attribute_num - 1
                else: self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_num)):
            # Horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_num
            left = (item * increment) + (increment -  self.width) // 2

            # Vertical position
            top = self.display_surface.get_size()[1] * 0.1

            # Create the object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for item in self.item_list:
            item.display(self.display_surface, 0, 'test', 1, 2, 3)


class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display(self, surface, selection_num, name, value, max_value, cost):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)