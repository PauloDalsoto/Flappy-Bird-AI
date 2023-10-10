import pygame
import os
import random

class Pipe:
    # Distância padrão entre os canos e velocidade de movimento
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        # Carrega a imagem do cano
        IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))

        self.x = x
        self.height = 0
        self.top_position = 0
        self.base_position = 0
        self.TOP_PIPE = pygame.transform.flip(IMAGE_PIPE, False, True)
        self.BASE_PIPE = IMAGE_PIPE
        self.passed = False
        self.set_height()

    def set_height(self):
        # Define aleatoriamente a altura do cano e suas posições superior e inferior
        self.height = random.randrange(50, 450)
        self.top_position = self.height - self.TOP_PIPE.get_height()
        self.base_position = self.height + self.DISTANCE

    def move(self):
        # Move o cano para a esquerda
        self.x -= self.SPEED

    def draw(self, screen):
        # Desenha o cano na tela
        screen.blit(self.TOP_PIPE, (self.x, self.top_position))
        screen.blit(self.BASE_PIPE, (self.x, self.base_position))

    def collide(self, bird):
        # Verifica a colisão entre o pássaro e o cano
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BASE_PIPE)

        top_distance = (self.x - bird.x, self.top_position - round(bird.y))
        base_distance = (self.x - bird.x, self.base_position - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_distance)
        base_point = bird_mask.overlap(base_mask, base_distance)

        if top_point or base_point:
            return True
        else:
            return False
