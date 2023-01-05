import pygame,time,sys
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_weapon):
        super().__init__(groups)
        self.display_surface=pygame.display.get_surface()
        self.image=pygame.image.load('up_idle/0.png').convert_alpha()
        self.enlarge=(96,96)
        self.image=pygame.transform.scale(self.image,self.enlarge)
        self.direction=pygame.math.Vector2()#this will give the position of the player
        self.rect=self.image.get_rect(topleft=pos)
        self.obstacle_sprites=obstacle_sprites
        self.hitbox=self.rect.inflate(-54,-32)
        self.create_attack=create_attack
        self.destroy_weapon=destroy_weapon
        
        #audio
        #stats
        self.speed=5
        self.damage=10
        self.health=3

        #movement
        self.attacking=False
        self.attack_cd=400
        self.attack_time=pygame.time.get_ticks()

        #animation images
        self.walk_left=[
            pygame.image.load('side_walk/0.png').convert_alpha(),
            pygame.image.load('side_walk/1.png').convert_alpha(),
            pygame.image.load('side_walk/2.png').convert_alpha(),
            pygame.image.load('side_walk/3.png').convert_alpha(),
            pygame.image.load('side_walk/4.png').convert_alpha(),
            pygame.image.load('side_walk/5.png').convert_alpha(),
            ]   
        self.walk_right=[
            pygame.image.load('side_walk1/0.png').convert_alpha(),
            pygame.image.load('side_walk1/1.png').convert_alpha(),
            pygame.image.load('side_walk1/2.png').convert_alpha(),
            pygame.image.load('side_walk1/3.png').convert_alpha(),
            pygame.image.load('side_walk1/4.png').convert_alpha(),
            pygame.image.load('side_walk1/5.png').convert_alpha(),
            ]
        self.down_attack=[
            pygame.image.load('down_attack/0.png').convert_alpha(),
            pygame.image.load('down_attack/1.png').convert_alpha(),
            pygame.image.load('down_attack/2.png').convert_alpha(),
        ]    
        self.up_attack=[
            pygame.image.load('up_attack/0.png').convert_alpha(),
            pygame.image.load('up_attack/1.png').convert_alpha(),
            pygame.image.load('up_attack/2.png').convert_alpha(),
        ]  
        self.right_attack=[
            pygame.image.load('right_attack/0.png').convert_alpha(),
            pygame.image.load('right_attack/1.png').convert_alpha(),
            pygame.image.load('right_attack/2.png').convert_alpha(),
        ]  
        self.left_attack=[
            pygame.image.load('left_attack/0.png').convert_alpha(),
            pygame.image.load('left_attack/1.png').convert_alpha(),
            pygame.image.load('left_attack/2.png').convert_alpha(),
        ]  
        self.walk_up=[
            pygame.image.load('up_walk/0.png').convert_alpha(),
            pygame.image.load('up_walk/1.png').convert_alpha(),
            pygame.image.load('up_walk/2.png').convert_alpha(),
            pygame.image.load('up_walk/3.png').convert_alpha(),
            pygame.image.load('up_walk/4.png').convert_alpha(),
            pygame.image.load('up_walk/5.png').convert_alpha(),
        ]
        self.walk_down=[
            pygame.image.load('down_walk/0.png').convert_alpha(),
            pygame.image.load('down_walk/1.png').convert_alpha(),
            pygame.image.load('down_walk/2.png').convert_alpha(),
            pygame.image.load('down_walk/3.png').convert_alpha(),
            pygame.image.load('down_walk/4.png').convert_alpha(),
            pygame.image.load('down_walk/5.png').convert_alpha(),
        ]
        self.up_idle=[
            pygame.image.load('up_idle/0.png').convert_alpha(),
            pygame.image.load('up_idle/1.png').convert_alpha(),
            pygame.image.load('up_idle/2.png').convert_alpha(),
            pygame.image.load('up_idle/3.png').convert_alpha(),
            pygame.image.load('up_idle/4.png').convert_alpha(),
        ]
        self.down_idle=[
            pygame.image.load('down_idle/0.png').convert_alpha(),
            pygame.image.load('down_idle/1.png').convert_alpha(),
            pygame.image.load('down_idle/2.png').convert_alpha(),
            pygame.image.load('down_idle/3.png').convert_alpha(),
            pygame.image.load('down_idle/4.png').convert_alpha(),
        ]
        self.left_idle=[
            pygame.image.load('left_idle/0.png').convert_alpha(),
            pygame.image.load('left_idle/1.png').convert_alpha(),
            pygame.image.load('left_idle/2.png').convert_alpha(),
            pygame.image.load('left_idle/3.png').convert_alpha(),
            pygame.image.load('left_idle/4.png').convert_alpha(),
        ]
        self.right_idle=[
            pygame.image.load('right_idle/0.png').convert_alpha(),
            pygame.image.load('right_idle/1.png').convert_alpha(),
            pygame.image.load('right_idle/2.png').convert_alpha(),
            pygame.image.load('right_idle/3.png').convert_alpha(),
            pygame.image.load('right_idle/4.png').convert_alpha(),
        ]
        
        #Character animations
        self.index=0
        self.animation_timer=time.perf_counter()
        self.animation_delay=0.2
        self.status='up'

    def cooldown(self):
        current_time=pygame.time.get_ticks()
        if self.attacking:
            if current_time-self.attack_time>=self.attack_cd:
                self.attacking=False
                self.destroy_weapon()

    def input(self):
        #movement
        keys=pygame.key.get_pressed()
        if not self.attacking:
            if keys[pygame.K_w]:
                self.direction.y=-1
                self.status='up'
                self.player_animation(self.status)

            elif keys[pygame.K_s]:
                self.direction.y=1
                self.status='down'
                self.player_animation(self.status)

            else:
                self.direction.y=0
        
            if keys[pygame.K_d]:
                self.direction.x=1
                self.status='right'
                self.player_animation(self.status)

            elif keys[pygame.K_a]:
                self.direction.x=-1
                self.status='left'
                self.player_animation(self.status)

            else:
                self.direction.x=0

            if keys[pygame.K_k]:
                pygame.quit()
                sys.exit()
        
        if self.direction.x == 0 and self.direction.y==0:
            self.player_animation(self.status)

        
        #attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attack_time=pygame.time.get_ticks()
            self.attacking=True
            self.player_animation(self.status)
            self.create_attack()


    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction=self.direction.normalize()
        self.hitbox.x+=self.direction.x*speed
        self.check_collide("horizontal")
        self.hitbox.y+=self.direction.y*speed
        self.check_collide("veritcal")
        self.rect.center=self.hitbox.center


    def update(self):
        self.input()
        self.get_status()
        self.move(self.speed)
        self.cooldown()

    def check_collide(self,direction):
        if direction=="horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x>0: #player is moving to the right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x<0:
                        self.hitbox.left=sprite.hitbox.right

        
        if direction=="veritcal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y<0:
                        self.hitbox.top=sprite.hitbox.bottom
                    if self.direction.y>0:
                        self.hitbox.bottom=sprite.hitbox.top

    def player_animation(self, animation_type):
        """Plays the specified animation."""

        if animation_type == "left" :
            self.image = self.walk_left[self.index]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.walk_left):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "right" :
            self.image = self.walk_right[self.index]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.walk_right):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "up" :
            self.image = self.walk_up[self.index]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.walk_up):
                self.index = 0  # reset index when the animation is finished
                

        elif animation_type == "up_idle" :
            self.image = self.up_idle[self.index % len(self.up_idle)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.up_idle):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "down" :
            self.image = self.walk_down[self.index % len(self.walk_down)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.walk_down):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "down_attack" :
            self.image = self.down_attack[self.index % len(self.down_attack)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.down_attack):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "up_attack" :
            self.image = self.up_attack[self.index % len(self.up_attack)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.up_attack):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "right_attack" :
            self.image = self.right_attack[self.index % len(self.right_attack)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.right_attack):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "left_attack" :
            self.image = self.left_attack[self.index % len(self.left_attack)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.left_attack):
                self.index = 0  # reset index when the animation is finished


        elif animation_type == "down_idle" :
            self.image = self.down_idle[self.index % len(self.down_idle)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.down_idle):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "left_idle" :
            self.image = self.left_idle[self.index % len(self.left_idle)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.left_idle):
                self.index = 0  # reset index when the animation is finished

        elif animation_type == "right_idle" :
            self.image = self.right_idle[self.index % len(self.right_idle)]
            self.image = pygame.transform.scale(self.image,self.enlarge)
            current_time=time.perf_counter()
            if current_time-self.animation_timer>=self.animation_delay:
                self.index += 1
                self.animation_timer=time.perf_counter()
            if self.index >= len(self.right_idle):
                self.index = 0  # reset index when the animation is finished
                
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and not ('idle' in self.status or 'attack' in self.status):
            self.status += '_idle'
        elif self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'idle' in self.status:
                self.status = self.status.replace('_idle', '_attack')
            elif not '_attack' in self.status:
                self.status += '_attack'
        elif 'attack' in self.status:
            self.status = self.status.replace('_attack', '_idle')
