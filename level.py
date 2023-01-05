import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from filereader import import_csv_layout
from weapon import weapon
from ui import UI

class Level:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        #sprite group setup
        self.visible_sprites=YCamera()
        self.obstacle_sprites=pygame.sprite.Group()
        self.current_attack=None
        self.UI=UI()
        
        #sprite setup
        self.create_map()
        
    def create_map(self):

        layout = {
            'boundary': import_csv_layout('map/Map_FloorBlocks.csv'),
            'flowers': import_csv_layout('map/Map_Extra.csv'),
            'details': import_csv_layout('map/Map_Details.csv')
        }

        file_paths = {
            '567': 'details/shadow.png',
            '166': 'details/house0.png',
            '167': 'details/house1.png',
            '168': 'details/house2.png',
            '169': 'details/house3.png',
            '170': 'details/house4.png',
            '126': 'details/house5.png',
            '127': 'details/house6.png',
            '128': 'details/house7.png',
            '129': 'details/house8.png',
            '130': 'details/house9.png',
            '86': 'details/house10.png',
            '87': 'details/house11.png',
            '88': 'details/house12.png',
            '89': 'details/house13.png',
            '90': 'details/house14.png',
            '46': 'details/house15.png',
            '47': 'details/house16.png',
            '48': 'details/house17.png',
            '49': 'details/house18.png',
            '50': 'details/house19.png',
            '6': 'details/house20.png',
            '7': 'details/house21.png',
            '8': 'details/house22.png',
            '9': 'details/house23.png',
            '10': 'details/house24.png',
            '1125': 'details/flag0.png',
            '1085': 'details/flag1.png',
}

        for style,layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col!='-1' and col!='2':
                        x = col_index*TILESIZE
                        y = row_index*TILESIZE
                        if style=='boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style=='flowers':
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'flowers',pygame.image.load('map/Bush.png').convert_alpha())
                        if style=='details':
                            file_path = file_paths.get(col)
                            if file_path:
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'house',pygame.image.load(file_path).convert_alpha())
        
        self.player=Player((1460,470),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_weapon)


    def run(self):
        self.visible_sprites.drawing(self.player)
        self.visible_sprites.update()
        self.UI.display(self.player)
        debug(self.player.status)

    def create_attack(self):
        self.current_attack=weapon(self.player,self.visible_sprites)
    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack=None



class YCamera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.half_width=self.display_surface.get_size()[0] // 2
        self.half_height=self.display_surface.get_size()[1] // 2
        self.offset=pygame.math.Vector2()

        self.floor_surf=pygame.image.load('map/map6.png')
        self.floor_rect=self.floor_surf.get_rect(topleft=(0,0))
    
    def drawing(self,player):

        #getting the offset
        self.offset.x=player.rect.centerx - self.half_width 
        self.offset.y=player.rect.centery - self.half_height

        floor_offset_pos= self.floor_rect.topleft-self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)


        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            offset_pos=sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)