import pygame,sys,time
from debug import debug

class weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]
        self.image=pygame.image.load('gfx/empty.png')
        if direction=='right':
            self.rect=self.image.get_rect(center=player.rect.midright)
        
        elif direction=='left':
            self.rect=self.image.get_rect(center=player.rect.midleft)
        elif direction=='up':
            self.rect=self.image.get_rect(center=player.rect.midtop)
        elif direction=='down':
            self.rect=self.image.get_rect(center=player.rect.midbottom)
        else:
            print('error, game closing in 3 seconds')
            time.sleep(3)
            exit()