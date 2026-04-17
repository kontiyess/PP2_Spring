import pygame
import datetime
import math


class Clock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.seconds = 0
        self.minutes = 0

    def update(self):
        now = datetime.datetime.now()
        self.seconds = now.second
        self.minutes = now.minute

    def draw(self, screen):
        screen.fill((255, 255, 255))

        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 120, 3)

        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = self.x + math.cos(angle) * 95
            y1 = self.y + math.sin(angle) * 95
            x2 = self.x + math.cos(angle) * 110
            y2 = self.y + math.sin(angle) * 110
            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 3)

        sec_angle = math.radians(self.seconds * 6 - 90)
        min_angle = math.radians(self.minutes * 6 - 90)

        sec_x = self.x + math.cos(sec_angle) * 100
        sec_y = self.y + math.sin(sec_angle) * 100
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (sec_x, sec_y), 2)

        min_x = self.x + math.cos(min_angle) * 70
        min_y = self.y + math.sin(min_angle) * 70
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (min_x, min_y), 5)

        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 6)