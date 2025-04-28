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

# متغيرات إضافية
scale_factor = 1  # للتحجيم
shear_x = 0       # للقص
rotation_angle = 0  # للدوران

# الشخص الثاني: دوال الرسم
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

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

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

# الشخص الثالث: دوال الحركة والتصادم
def move_snake(snake, direction, food):
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]

    # إذا اصطدم الثعبان بالحواف
    if head_x >= WIDTH or head_x < 0:
        direction = (-direction[0], direction[1])  # انعكاس في الاتجاه الأفقي
        head_x = snake[0][0] + direction[0]  # إعادة الثعبان لمكانه الجديد
    if head_y >= HEIGHT or head_y < 0:
        direction = (direction[0], -direction[1])  # انعكاس في الاتجاه الرأسي
        head_y = snake[0][1] + direction[1]  # إعادة الثعبان لمكانه الجديد

    head = (head_x, head_y)
    snake.insert(0, head)
    if head == food:
        return True, direction
    else:
        snake.pop()
        return False, direction

def spawn_food(snake):
    while True:
        pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        if pos not in snake:
            return pos

def check_collision(snake):
    head = snake[0]
    # الثعبان يخسر فقط إذا اصطدم بنفسه
    return head in snake[1:]

# الشخص الرابع: الحلقة الرئيسية
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
            # عكس الاتجاه فور الاصطدام
            direction = (-direction[0], -direction[1])  # انعكاس الاتجاه
            # تحديث مكان الرأس ليعكس الاتجاه
            head_x = snake[0][0] + direction[0]
            head_y = snake[0][1] + direction[1]
            snake[0] = (head_x, head_y)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
