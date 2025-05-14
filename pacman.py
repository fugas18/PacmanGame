import pygame
import random
import math

# Inicializando o Pygame
pygame.init()

# Definir as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Tamanho da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Criar a tela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Básico")

# Definir o relógio para controlar a taxa de quadros
clock = pygame.time.Clock()

# Função para desenhar o Pac-Man
def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), 20)

# Função para desenhar a comida
def draw_food(x, y):
    pygame.draw.circle(screen, BLUE, (x, y), 10)

# Função para desenhar o fantasma
def draw_ghost(x, y):
    pygame.draw.circle(screen, RED, (x, y), 20)

# Função para mover o fantasma em direção ao Pac-Man
def move_ghost(ghost_x, ghost_y, pacman_x, pacman_y, speed=2):
    # Calcular a diferença de posição
    dx = pacman_x - ghost_x
    dy = pacman_y - ghost_y

    # Calcular a distância entre o fantasma e o Pac-Man
    distance = math.sqrt(dx**2 + dy**2)

    # Normalizar a direção do movimento
    if distance != 0:
        dx /= distance
        dy /= distance

    # Mover o fantasma na direção do Pac-Man
    ghost_x += dx * speed
    ghost_y += dy * speed

    return ghost_x, ghost_y

# Função principal do jogo
def game_loop():
    # Coordenadas iniciais do Pac-Man
    pacman_x = SCREEN_WIDTH // 2
    pacman_y = SCREEN_HEIGHT // 2

    pacman_dx = 0
    pacman_dy = 0

    # Coordenadas da comida
    food_x = random.randint(20, SCREEN_WIDTH - 20)
    food_y = random.randint(20, SCREEN_HEIGHT - 20)

    # Inicializando os fantasmas (mais de um fantasma)
    ghosts = [
        {'x': random.randint(20, SCREEN_WIDTH - 20), 'y': random.randint(20, SCREEN_HEIGHT - 20)},
        {'x': random.randint(20, SCREEN_WIDTH - 20), 'y': random.randint(20, SCREEN_HEIGHT - 20)}
    ]

    # Pontuação
    score = 0

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman_dx = -5
                    pacman_dy = 0
                if event.key == pygame.K_RIGHT:
                    pacman_dx = 5
                    pacman_dy = 0
                if event.key == pygame.K_UP:
                    pacman_dy = -5
                    pacman_dx = 0
                if event.key == pygame.K_DOWN:
                    pacman_dy = 5
                    pacman_dx = 0

        # Atualizar a posição do Pac-Man
        pacman_x += pacman_dx
        pacman_y += pacman_dy

        # Verificar colisão com as bordas
        if pacman_x < 0:
            pacman_x = 0
        if pacman_x > SCREEN_WIDTH:
            pacman_x = SCREEN_WIDTH
        if pacman_y < 0:
            pacman_y = 0
        if pacman_y > SCREEN_HEIGHT:
            pacman_y = SCREEN_HEIGHT

        # Verificar colisão com a comida
        if abs(pacman_x - food_x) < 20 and abs(pacman_y - food_y) < 20:
            food_x = random.randint(20, SCREEN_WIDTH - 20)
            food_y = random.randint(20, SCREEN_HEIGHT - 20)
            score += 1

        # Verificar colisão com os fantasmas
        for ghost in ghosts:
            if abs(pacman_x - ghost['x']) < 20 and abs(pacman_y - ghost['y']) < 20:
                game_running = False
                print("Game Over! Pontuação final:", score)

            # Mover o fantasma em direção ao Pac-Man
            ghost['x'], ghost['y'] = move_ghost(ghost['x'], ghost['y'], pacman_x, pacman_y)

        # Atualizar a tela
        screen.fill(BLACK)

        # Desenhar o Pac-Man, comida e fantasmas
        draw_pacman(pacman_x, pacman_y)
        draw_food(food_x, food_y)
        for ghost in ghosts:
            draw_ghost(ghost['x'], ghost['y'])

        # Exibir a pontuação
        font = pygame.font.SysFont("Arial", 25)
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Atualizar a tela
        pygame.display.update()

        # Controlar a taxa de quadros
        clock.tick(30)

    pygame.quit()

# Iniciar o jogo
game_loop()
