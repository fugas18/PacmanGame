import pygame
import random
import math

# Inicializando o Pygame
pygame.init()

# Constantes
TILE_SIZE = 40
MAP_WIDTH = 15
MAP_HEIGHT = 15
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Criar tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Básico")
clock = pygame.time.Clock()

# Mapa (0 = caminho, 1 = parede)
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Funções auxiliares
def draw_tile_map():
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            if MAP[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), TILE_SIZE//2 - 4)

def draw_food(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 5)

def draw_ghost(ghost):
    pygame.draw.circle(screen, ghost['color'], (int(ghost['x']), int(ghost['y'])), TILE_SIZE//2 - 4)

def is_centered(x, y):
    return x % TILE_SIZE == TILE_SIZE // 2 and y % TILE_SIZE == TILE_SIZE // 2

def can_move(x, y):
    # Margem de segurança para evitar entrar na parede
    radius = TILE_SIZE // 2 - 4
    # Pegar os quatro cantos da circunferência (bounding box)
    corners = [
        (x - radius, y - radius),
        (x + radius, y - radius),
        (x - radius, y + radius),
        (x + radius, y + radius),
    ]
    for cx, cy in corners:
        col = cx // TILE_SIZE
        row = cy // TILE_SIZE
        if not (0 <= row < MAP_HEIGHT and 0 <= col < MAP_WIDTH and MAP[row][col] == 0):
            return False
    return True


# Função principal do jogo
def game_loop():
    pacman_x = TILE_SIZE * 1 + TILE_SIZE // 2
    pacman_y = TILE_SIZE * 1 + TILE_SIZE // 2
    pacman_dx, pacman_dy = 0, 0

    foods = []
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            if MAP[row][col] == 0:
                foods.append({'x': col * TILE_SIZE + TILE_SIZE // 2, 'y': row * TILE_SIZE + TILE_SIZE // 2})

    ghosts = []
    types = ['chaser', 'random', 'trailer']
    colors = [RED, BLUE, GREEN]

    for i in range(3):
        while True:
            gx = random.randint(0, MAP_WIDTH - 1)
            gy = random.randint(0, MAP_HEIGHT - 1)
            if MAP[gy][gx] == 0:
                ghosts.append({
                    'x': gx * TILE_SIZE + TILE_SIZE // 2,
                    'y': gy * TILE_SIZE + TILE_SIZE // 2,
                    'type': types[i],
                    'color': colors[i],
                    'dir': random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                })
                break

    score = 0
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN and is_centered(pacman_x, pacman_y):
                if event.key == pygame.K_LEFT:
                    if can_move(pacman_x - TILE_SIZE, pacman_y):
                        pacman_dx = -TILE_SIZE // 8
                        pacman_dy = 0
                if event.key == pygame.K_RIGHT:
                    if can_move(pacman_x + TILE_SIZE, pacman_y):
                        pacman_dx = TILE_SIZE // 8
                        pacman_dy = 0
                if event.key == pygame.K_UP:
                    if can_move(pacman_x, pacman_y - TILE_SIZE):
                        pacman_dy = -TILE_SIZE // 8
                        pacman_dx = 0
                if event.key == pygame.K_DOWN:
                    if can_move(pacman_x, pacman_y + TILE_SIZE):
                        pacman_dy = TILE_SIZE // 8
                        pacman_dx = 0

        # Movimento do Pac-Man
        next_px = pacman_x + pacman_dx
        next_py = pacman_y + pacman_dy
        if can_move(next_px, next_py):
            pacman_x = next_px
            pacman_y = next_py
        else:
            pacman_dx = 0
            pacman_dy = 0

        # Verificar coleta de comida
        for food in foods[:]:
            if abs(pacman_x - food['x']) < TILE_SIZE // 2 and abs(pacman_y - food['y']) < TILE_SIZE // 2:
                foods.remove(food)
                score += 1

        # Atualizar fantasmas
        for ghost in ghosts:
            if is_centered(ghost['x'], ghost['y']):
                possible_dirs = [(1,0), (-1,0), (0,1), (0,-1)]
                random.shuffle(possible_dirs)
                for dx, dy in possible_dirs:
                    new_x = ghost['x'] + dx * TILE_SIZE
                    new_y = ghost['y'] + dy * TILE_SIZE
                    if can_move(new_x, new_y):
                        ghost['dir'] = (dx, dy)
                        break
            ghost['x'] += ghost['dir'][0] * TILE_SIZE // 8
            ghost['y'] += ghost['dir'][1] * TILE_SIZE // 8

            # Verificar colisão com o Pac-Man
            if abs(pacman_x - ghost['x']) < TILE_SIZE // 2 and abs(pacman_y - ghost['y']) < TILE_SIZE // 2:
                game_running = False
                print("Game Over! Pontuação:", score)

        screen.fill(BLACK)
        draw_tile_map()
        for food in foods:
            draw_food(food['x'], food['y'])
        for ghost in ghosts:
            draw_ghost(ghost)
        draw_pacman(pacman_x, pacman_y)

        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

# Iniciar o jogo
game_loop()
