import pygame
from clock import Clock

pygame.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()
mickey_clock = Clock(WIDTH // 2, HEIGHT // 2)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey_clock.update()
    mickey_clock.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()