import pygame
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from support import *
from random import choice
from weapon import Weapon
from ui import UI
from debug import debug

class Level:
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack Sprites
        self.current_attack = None

        # Sprite main setup
        self.create_map()

        # User interface
        self.ui = UI()

    def create_map(self):
        # Create a dictionary of layouts from imported files to find WHERE to layer on game surface
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }

        # Create a dictionary of graphics/images to USE when layering/creating game surface map
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'grass':
                            random_grass = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass)

                        if style == 'object':
                            surf_objects = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf_objects)

                        if style == 'entities':
                            if col == PLAYER_TILE_ID:
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic
                                )
                            else:
                                if col == BAMBOO_TILE_ID: monster_name = 'bamboo'
                                elif col == SPIRIT_TILE_ID: monster_name = 'spirit'
                                elif col == RACCOON_TILE_ID: monster_name = 'raccoon'
                                elif col == SQUID_TILE_ID: monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites], self.obstacle_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        print(style, strength, cost)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # General setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Get width, height, and offset
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Create the floor image
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        # Get offset from the player object/class
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw the floor map
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Draw all sprites by order of y-values, so drawing overlap looks correct
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            sprite_offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, sprite_offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)