import pygame
import random
import sys
import math

pygame.init()

# شاشة اللعبة
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game Transformations')

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

# متغيرات إضافية (التحجيم، القص، والدوران)
scale_factor = 1
shear_x = 0
rotation_angle = 0

# دالة رسم الثعبان
def draw_snake(snake, scale_factor, shear_x, rotation_angle):
    for segment in snake:
        rect = pygame.Rect(segment[0], segment[1], CELL_SIZE * scale_factor, CELL_SIZE)
        points = [
            (rect.left + shear_x, rect.top),
            (rect.right + shear_x, rect.top),
            (rect.right - shear_x, rect.bottom),
            (rect.left - shear_x, rect.bottom)
        ]
        rotated_points = rotate_points(points, rect.center, rotation_angle)
        pygame.draw.polygon(screen, GREEN, rotated_points)

# دالة رسم الطعام
def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

# دالة رسم النقاط
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# دالة لتدوير النقاط
def rotate_points(points, center, angle):
    rad = math.radians(angle)
    cos_theta = math.cos(rad)
    sin_theta = math.sin(rad)
    cx, cy = center
    rotated = []
    for x, y in points:
        x -= cx
        y -= cy
        x_new = x * cos_theta - y * sin_theta
        y_new = x * sin_theta + y * cos_theta
        rotated.append((x_new + cx, y_new + cy))
    return rotated

# دالة لتحريك الثعبان (الانعكاس عند الحواف)
def move_snake(snake, direction, food):
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]

    # التحقق من الاصطدام بالحواف مع ارتداد سريع (بدون إنهاء اللعبة)
    if head_x >= WIDTH:  # اصطدام الجدار الأيمن
        direction = (-direction[0], direction[1])  # انعكاس في الاتجاه الأفقي
    if head_x < 0:  # اصطدام الجدار الأيسر
        direction = (-direction[0], direction[1])  # انعكاس في الاتجاه الأفقي
    if head_y >= HEIGHT:  # اصطدام الجدار السفلي
        direction = (direction[0], -direction[1])  # انعكاس في الاتجاه الرأسي
    if head_y < 0:  # اصطدام الجدار العلوي
        direction = (direction[0], -direction[1])  # انعكاس في الاتجاه الرأسي

    head = (head_x, head_y)
    snake.insert(0, head)
    if head == food:
        return True, direction
    else:
        snake.pop()
        return False, direction

# دالة لتوليد الطعام في مكان عشوائي
def spawn_food(snake):
    while True:
        pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        if pos not in snake:
            return pos

# دالة للتحقق من التصادم مع نفسه
def check_collision(snake):
    head = snake[0]
    return head in snake[1:]

# دالة للتعامل مع الضغط على الأزرار
def handle_keys(direction):
    global rotation_angle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
        return (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
        return (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
        return (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
        return (CELL_SIZE, 0)
    if keys[pygame.K_SPACE]:
        rotation_angle += 10  # دوران مع كل ضغطة على المسافة
    return direction

# دالة لإظهار شاشة "Game Over"
def game_over():
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # انتظار لثانيتين قبل الخروج

# الدالة الرئيسية لتشغيل اللعبة
def main():
    global direction, snake, food, score, scale_factor, shear_x
    running = True
    while running:
        screen.fill(BLACK)
        draw_snake(snake, scale_factor, shear_x, rotation_angle)
        draw_food(food)
        draw_score(score)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        direction = handle_keys(direction)

        ate_food, direction = move_snake(snake, direction, food)
        if ate_food:
            food = spawn_food(snake)
            score += 1
            scale_factor += 0.05  # تحجيم مع الأكل
            shear_x += 0.5        # زيادة القص كل مرة يأكل فيها

        # التحقق من التصادم مع نفسه
        if check_collision(snake):
            game_over()  # إظهار شاشة "Game Over" عند التصادم
            break  # الخروج من اللعبة إذا اصطدم الثعبان بنفسه

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
