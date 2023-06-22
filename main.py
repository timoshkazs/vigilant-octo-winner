import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Определение размеров блока тетриса
BLOCK_SIZE = 30

# Определение размеров сетки
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Определение начальной позиции фигуры
INITIAL_X = GRID_WIDTH // 2 - 1
INITIAL_Y = 0

# Определение возможных фигур тетриса и их цветов
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE]

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Функция создания новой фигуры
def create_new_piece():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    x = INITIAL_X
    y = INITIAL_Y
    return shape, color, x, y

# Функция отрисовки сетки
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

# Функция отрисовки текущей фигуры
def draw_piece(shape, color, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE + col * BLOCK_SIZE, y * BLOCK_SIZE + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Функция проверки столкновений
def check_collision(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col] != BLACK:
                    return True
    return False

# Функция обновления сетки
def update_grid(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                grid[y + row][x + col] = shape[row][col]

# Функция удаления заполненных линий
def remove_lines():
    full_rows = []
    for row in range(GRID_HEIGHT):
        if all(cell != BLACK for cell in grid[row]):
            full_rows.append(row)
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)

# Инициализация сетки
grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Инициализация текущей фигуры
current_shape, current_color, current_x, current_y = create_new_piece()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_shape, current_x - 1, current_y):
                    current_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_shape, current_x + 1, current_y):
                    current_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_shape, current_x, current_y + 1):
                    current_y += 1
            elif event.key == pygame.K_SPACE:
                rotated_shape = [[current_shape[j][i] for j in range(len(current_shape))] for i in range(len(current_shape[0]))]
                if not check_collision(rotated_shape, current_x, current_y):
                    current_shape = rotated_shape

    if not check_collision(current_shape, current_x, current_y + 1):
        current_y += 1
    else:
        update_grid(current_shape, current_x, current_y)
        remove_lines()
        current_shape, current_color, current_x, current_y = create_new_piece()
        if check_collision(current_shape, current_x, current_y):
            running = False

    screen.fill(BLACK)
    draw_grid()
    draw_piece(current_shape, current_color, current_x, current_y)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != BLACK:
                pygame.draw.rect(screen, grid[row][col], (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()
    clock.tick(10)

# Завершение игры
pygame.quit()
