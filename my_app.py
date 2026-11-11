import pygame
from random import randrange

# Ініціалізація Pygame[cite: 4]
pygame.init()

# --- Параметри ---
CELL = 20
COLS, ROWS = 20, 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змійка")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# --- Кольори (запасний варіант, якщо немає картинок) ---
BG_COLOR = (200, 255, 200)
SNAKE_COLOR = (0, 150, 0)
APPLE_COLOR = (200, 0, 0)

# --- Завантаження картинок (опціонально) ---
# Покладіть файли background.png, snake.png, apple.png у папку з проєктом
try:
    bg_img = pygame.image.load("background.png").convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
except Exception:
    bg_img = pygame.image.load("dvor.png").convert()
    
    

try:
    snake_img = pygame.image.load("snake.png").convert_alpha()
    snake_img = pygame.transform.scale(snake_img, (CELL, CELL))
except Exception:
    snake_img = pygame.image.load("zmeja.png").convert_alpha()

try:
    apple_img = pygame.image.load("apple.png").convert_alpha()
    apple_img = pygame.transform.scale(apple_img, (CELL, CELL))
except Exception:
    apple_img = pygame.image.load("jabluko.png").convert_alpha()


# --- Нове яблуко (не під змійкою) ---
def new_apple(snake):
    while True:
        pos = (randrange(0, COLS) * CELL, randrange(0, ROWS) * CELL)
        if pos not in snake:
            return pos


# --- Початкові об'єкти ---
snake = [((COLS // 2) * CELL, (ROWS // 2) * CELL)]
dx, dy = 1, 0
apple = new_apple(snake)
score = 0

start_ticks = pygame.time.get_ticks()
finish_ticks = start_ticks

running = True
win = False
game_over = False

while running:
    # --- Події ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = 1, 0
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -1, 0
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -1
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, 1

    if not win and not game_over:
        # --- Рух змійки ---
        head_x, head_y = snake[-1]
        new_head = (head_x + dx * CELL, head_y + dy * CELL)
        snake.append(new_head)

        # --- Вихід за межі ---
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            game_over = True
            finish_ticks = pygame.time.get_ticks()

        # --- Зіткнення з тілом ---
        for part in snake[:-1]:
            if new_head == part:
                game_over = True
                finish_ticks = pygame.time.get_ticks()

        # --- Яблуко ---
        if new_head == apple:
            score += 1
            apple = new_apple(snake)
            if score >= 10:
                win = True
                finish_ticks = pygame.time.get_ticks()
        else:
            snake.pop(0)

    # --- Відображення фону (картинка або колір) ---
    if bg_img:
        screen.blit(bg_img, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # --- Малюємо змійку (картинка або прямокутник) ---
    for x, y in snake:
        if snake_img:
            screen.blit(snake_img, (x, y))
        else:
            pygame.draw.rect(screen, SNAKE_COLOR, (x, y, CELL, CELL))

    # --- Малюємо яблуко (картинка або прямокутник) ---
    if apple_img:
        screen.blit(apple_img, apple)
    else:
        pygame.draw.rect(screen, APPLE_COLOR, (*apple, CELL, CELL))

    if not game_over and not win:
        # --- Рахунок і час ---
        current_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        screen.blit(
            font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10)
        )
        screen.blit(
            font.render(f"Time: {current_seconds}s", True, (0, 0, 0)),
            (10, 40),
        )
    else:
        # --- Екран кінця гри ---
        total_time = (finish_ticks - start_ticks) // 1000
        if win:
            msg = font.render("ТИ ПЕРЕМІГ!", True, (0, 150, 0))
        else:
            msg = font.render("ГРА ЗАКІНЧЕНА", True, (200, 0, 0))

        time_text = font.render(f"Час: {total_time} с", True, (0, 0, 0))

        screen.blit(
            msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        )
        screen.blit(
            time_text,
            time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)),
        )

    pygame.display.update()
    clock.tick(5)