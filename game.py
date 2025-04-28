# الإعدادات والتهيئة
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

# الثعبان والطعام
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

# إطار اللعبة
clock = pygame.time.Clock()
FPS = 10

