import pygame
from typing import Tuple

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (40, 120, 220)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface, font):
        mouse = pygame.mouse.get_pos()
        color = BLUE if self.rect.collidepoint(mouse) else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

        txt = font.render(self.text, True, BLACK)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_text(surface, text, font, color, x, y, center=False):
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    rect.center = (x, y) if center else (x, y)
    surface.blit(txt, rect)