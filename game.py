# الشخص الأول: الإعدادات والتهيئة
import pygame
import random
import sys

pygame.init()

# شاشة اللعبة
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# ألوان
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# الثعبان والطعام
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

# إطار اللعبة
clock = pygame.time.Clock()
FPS = 10

# نقاط اللاعب
score = 0
font = pygame.font.SysFont(None, 35)

# الشخص الثاني: دوال الرسم
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# الشخص الثالث: دوال الحركة والتصادم
def move_snake(snake, direction, food):
    head_x = (snake[0][0] + direction[0]) % WIDTH
    head_y = (snake[0][1] + direction[1]) % HEIGHT
    head = (head_x, head_y)
    snake.insert(0, head)
    if head == food:
        return True
    else:
        snake.pop()
        return False

def spawn_food(snake):
    while True:
        pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        if pos not in snake:
            return pos

def check_collision(snake):
    head = snake[0]
    return head in snake[1:]

# الشخص الرابع: الحلقة الرئيسية
def handle_keys(direction):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
        return (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
        return (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
        return (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
        return (CELL_SIZE, 0)
    return direction

def main():
    global direction, snake, food, score
    running = True
    while running:
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        direction = handle_keys(direction)

        if move_snake(snake, direction, food):
            food = spawn_food(snake)
            score += 1

        if check_collision(snake):
            running = False

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
