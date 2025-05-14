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

# Tamanho da tela e dos blocos
TILE_SIZE = 30
MAP_WIDTH = 20
MAP_HEIGHT = 20
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

# Criar a tela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man com Labirinto")

# Definir o relógio para controlar a taxa de quadros
clock = pygame.time.Clock()

# Mapa do labirinto (1 = parede, 0 = caminho)
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,1,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1],
    [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,0,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Função para desenhar o mapa
def draw_map():
    for row_idx, row in enumerate(MAP):
        for col_idx, cell in enumerate(row):
            if cell == 1:
                rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, BLUE, rect)

# Verifica se uma coordenada é livre (sem parede)
def can_move(x, y):
    col = int(x) // TILE_SIZE
    row = int(y) // TILE_SIZE
    if 0 <= row < len(MAP) and 0 <= col < len(MAP[0]):
        return MAP[row][col] == 0
    return False

# Função para desenhar o Pac-Man
def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), 15)

# Função para desenhar a comida
def draw_food(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 5)

# Função para desenhar o fantasma
def draw_ghost(x, y):
    pygame.draw.circle(screen, RED, (x, y), 15)

# Função para mover o fantasma em direção ao Pac-Man
def move_ghost(ghost_x, ghost_y, pacman_x, pacman_y, speed=2):
    dx = pacman_x - ghost_x
    dy = pacman_y - ghost_y
    distance = math.hypot(dx, dy)
    if distance != 0:
        dx /= distance
        dy /= distance
    next_x = ghost_x + dx * speed
    next_y = ghost_y + dy * speed
    if can_move(next_x, next_y):
        return next_x, next_y
    return ghost_x, ghost_y

# Função principal do jogo
def game_loop():
    # Coordenadas iniciais do Pac-Man (centralizado em célula livre)
    pacman_x = TILE_SIZE * 1 + TILE_SIZE // 2
    pacman_y = TILE_SIZE * 1 + TILE_SIZE // 2
    pacman_dx, pacman_dy = 0, 0

    # Inicializando as comidas nas células livres do mapa
    foods = []
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            if MAP[row][col] == 0:
                foods.append({'x': col * TILE_SIZE + TILE_SIZE // 2, 'y': row * TILE_SIZE + TILE_SIZE // 2})

    # Inicializando os fantasmas (em posições aleatórias livres)
    ghosts = []
    for _ in range(3):
        while True:
            gx = random.randint(0, MAP_WIDTH - 1)
            gy = random.randint(0, MAP_HEIGHT - 1)
            if MAP[gy][gx] == 0:
                ghosts.append({'x': gx * TILE_SIZE + TILE_SIZE // 2, 'y': gy * TILE_SIZE + TILE_SIZE // 2})
                break

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

        # Atualizar a posição do Pac-Man com verificação de parede
        next_x = pacman_x + pacman_dx
        next_y = pacman_y + pacman_dy
        if can_move(next_x, next_y):
            pacman_x = next_x
            pacman_y = next_y

        # Atualizar os fantasmas
        for ghost in ghosts:
            ghost['x'], ghost['y'] = move_ghost(ghost['x'], ghost['y'], pacman_x, pacman_y)

        # Verificar colisão com as comidas
        for food in foods[:]:
            if abs(pacman_x - food['x']) < 15 and abs(pacman_y - food['y']) < 15:
                foods.remove(food)
                score += 1

        # Verificar colisão com os fantasmas
        for ghost in ghosts:
            if abs(pacman_x - ghost['x']) < 20 and abs(pacman_y - ghost['y']) < 20:
                print("Game Over! Pontuação final:", score)
                game_running = False

        # Atualizar a tela
        screen.fill(BLACK)
        draw_map()
        draw_pacman(pacman_x, pacman_y)
        for food in foods:
            draw_food(food['x'], food['y'])
        for ghost in ghosts:
            draw_ghost(ghost['x'], ghost['y'])

        # Exibir a pontuação
        font = pygame.font.SysFont("Arial", 25)
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

# Iniciar o jogo
game_loop()
