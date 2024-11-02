import pygame
from utils import load_spritesheet
from config import HEIGHT


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.speed = 2
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.run_frames=[]
        self.jump_frames = []
        self.damage_frames=[]
        self.death_frames=[]
        self.is_damaged = False
        self.is_dead = False
        self.damage_duration = 30  # Duración de la animación de daño en frames
        self.damage_counter = 0

        for num in range (1,8):
            img_run=pygame.image.load(f"assets/player1/run/Character2F_1_run_{num}.png")
            img_run =pygame.transform.scale(img_run, (self.width,self.height))
            self.run_frames.append(img_run)

        for num2 in range (1,3):
            img_jump=pygame.image.load(f"assets/player1/jump/Character2F_1_jump_{num2}.png")
            img_jump =pygame.transform.scale(img_jump, (self.width,self.height))
            self.jump_frames.append(img_jump)

        for num3 in range(1,3):
            
            img_damage=pygame.image.load(f"assets/player1/damage/Character2F_1_damage_{num3}.png")
            img_damage =pygame.transform.scale(img_damage, (self.width,self.height))
            self.damage_frames.append(img_damage)

        for num4 in range(0,9):
        
            img_death=pygame.image.load(f"assets/player1/death/Character2F_1_death_{num3}.png")
            img_death =pygame.transform.scale(img_death, (self.width,self.height))
            self.death_frames.append(img_death)
  
        self.hitbox_width = 40
        self.hitbox_height = 75

        self.frame_index = 0
        self.animation_speed = 0.3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        self.velocity_y += self.gravity
        self.y += self.velocity_y

        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True
        
        if self.is_damaged:
            self.damage_counter += 1
            if self.damage_counter >= self.damage_duration:
                self.is_damaged = False
                self.damage_counter = 0
    
    def die(self):
        self.is_dead = True
        self.frame_index = 0  

    def take_damage(self):
        self.is_damaged = True
        self.damage_counter = 0
    
    def reset_animation(self):
        self.frame_index = 0
        self.is_damaged = False
        self.is_dead = False
        self.damage_counter = 0
        self.on_ground = True



    def draw(self, surface):
        if self.is_dead:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.death_frames):
                self.frame_index = 0
        elif self.is_damaged:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.damage_frames):
              self.frame_index = 0  # Reinicia la animación al final
            frame = self.damage_frames[int(self.frame_index)]  # Mostrar el primer (y único) frame de daño
        elif self.on_ground:
            # Animación de correr
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.run_frames):
                self.frame_index = 0
            frame = self.run_frames[int(self.frame_index)]
        else:
            # Animación de salto
            frame = self.jump_frames[0]

        surface.blit(frame, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(
            self.x + (self.width - self.hitbox_width) // 2,
            self.y + (self.height - self.hitbox_height) // 2,
            self.hitbox_width,
            self.hitbox_height
        )
