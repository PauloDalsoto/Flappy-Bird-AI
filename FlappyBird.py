# Importa os módulos necessários
import pygame
import os
import neat

# Importa as classes personalizadas do jogo
from Bird import *
from Ground import *
from Pipe import *

# Variável que indica se a IA está jogando
AI_playing = True

# Variável que acompanha a geração atual
generation = 0

# Constantes do jogo
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Carrega a imagem de fundo e a redimensiona
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

# Inicializa a fonte para exibir a pontuação
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 50)


# Função para desenhar elementos na tela
def screen_draw(screen, birds, pipes, ground, score):
    # Desenha a imagem de fundo
    screen.blit(IMAGE_BACKGROUND, (0, 0))

    # Desenha todos os pássaros na tela
    for bird in birds:
        bird.draw(screen)

    # Desenha todos os canos na tela
    for pipe in pipes:
        pipe.draw(screen)

    # Exibe a pontuação na tela
    text = SCORE_FONT.render("Pontuação: {}".format(score), 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    # Se a IA estiver jogando, exibe o número da geração
    if AI_playing:
        text = SCORE_FONT.render("Geração: {}".format(generation), 1, (255, 255, 255))
        screen.blit(text, (10, 10))

    # Desenha o chão na tela
    ground.draw(screen)
    pygame.display.update()


# Função principal do jogo
def main(genomes, config):
    global generation
    generation += 1

    if AI_playing:
        networks = []
        genome_list = []
        birds = []

        # Inicializa as redes neurais, lista de genomas e pássaros
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)
            genome.fitness = 0
            genome_list.append(genome)
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]

    ground = Ground(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    game_clock = pygame.time.Clock()

    running = True
    while running:
        game_clock.tick(30)

        # Interação com o usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if not AI_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Faz com que todos os pássaros pulem quando a barra de espaço é pressionada
                        for bird in birds:
                            bird.jump()

        pipe_id = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].TOP_PIPE.get_width()):
                pipe_id = 1
        else:
            running = False
            break

        # Move os elementos do jogo
        for i, bird in enumerate(birds):
            bird.move()
            if AI_playing:
                genome_list[i].fitness += 0.1

                # Ativa a rede neural e decide se o pássaro deve pular ou não
                output = networks[i].activate((bird.y,
                                               abs(bird.y - pipes[pipe_id].height),
                                               abs(bird.y - pipes[pipe_id].base_position)))

                if output[0] > 0.5:
                    bird.jump()

        ground.move()

        put_pipe = False
        removed_pipes = []

        # Verifica colisões com os canos e remove pássaros se colidirem
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                    if AI_playing:
                        genome_list[i].fitness -= 1
                        genome_list.pop(i)
                        networks.pop(i)

                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    put_pipe = True
            pipe.move()
            if pipe.x + pipe.BASE_PIPE.get_width() < 0:
                removed_pipes.append(pipe)

        # Atualiza a pontuação e adiciona novos canos
        if put_pipe:
            score += 1
            pipes.append(Pipe(600))
            if AI_playing:
                for genome in genome_list:
                    genome.fitness += 5
        for pipe in removed_pipes:
            pipes.remove(pipe)

        # Remove pássaros que caíram no chão ou voaram para cima da tela
        for i, bird in enumerate(birds):
            if bird.y + bird.image.get_height() > ground.y or bird.y < 0:
                birds.pop(i)
                if AI_playing:
                    genome_list.pop(i)
                    networks.pop(i)

        # Chama a função para desenhar os elementos na tela
        screen_draw(screen, birds, pipes, ground, score)


# Função para executar o algoritmo genético
def run(config_file):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_file)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if AI_playing:
        population.run(main)
    else:
        main(None, None)


# Ponto de entrada do programa
if __name__ == '__main__':
    config_file = 'config.txt'
    run(config_file)
