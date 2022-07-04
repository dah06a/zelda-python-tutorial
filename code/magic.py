import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'flame': pygame.mixer.Sound('../audio/fire.wav')
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            offset = pygame.math.Vector2(0, -30)
            self.animation_player.create_particles('heal', player.rect.center + offset, groups)
        
    def flame(self, player, cost, groups):
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost

            pointing = player.status.split('_')[0]
            if pointing == 'up':
                direction = pygame.math.Vector2(0, -1)
            elif pointing == 'down':
                direction = pygame.math.Vector2(0, 1)
            elif pointing == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif pointing == 'right':
                direction = pygame.math.Vector2(1, 0)
            else:
                direction = pygame.math.Vector2(-1, 0)

            for i in range(1, 6):
                if direction.x:
                    offset_x = direction.x * TILESIZE * i
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:
                    offset_y = direction.y * TILESIZE * i
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)