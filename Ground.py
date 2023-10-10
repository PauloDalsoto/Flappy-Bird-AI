import pygame
import os

class Ground:
    # Carrega a imagem do chão e define constantes relacionadas
    IMAGE_GROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))

    SPEED = 5
    WIDTH = IMAGE_GROUND.get_width()
    IMAGE = IMAGE_GROUND

    def __init__(self, y):
        # Inicializa as propriedades do chão
        self.y = y
        self.x0 = 0
        self.x1 = self.WIDTH

    def move(self):
        # Move o chão para a esquerda
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED

        # Reinicia a posição do chão quando ele sai da tela
        if self.x0 + self.WIDTH < 0:
            self.x0 = self.x1 + self.WIDTH

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x0 + self.WIDTH

    def draw(self, screen):
        # Desenha o chão na tela
        screen.blit(self.IMAGE, (self.x0, self.y))
        screen.blit(self.IMAGE, (self.x1, self.y))
