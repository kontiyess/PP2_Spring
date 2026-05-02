import pygame
from collections import deque
import math

def draw_line(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)

def draw_rect(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end
    pygame.draw.rect(surface, color,
        (min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1)), size)

def draw_circle(surface, color, start, end, size):
    radius = int(math.hypot(end[0]-start[0], end[1]-start[1]))
    pygame.draw.circle(surface, color, start, radius, size)

def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    queue = deque([(x, y)])

    while queue:
        cx, cy = queue.popleft()

        if cx < 0 or cy < 0 or cx >= width or cy >= height:
            continue

        if surface.get_at((cx, cy)) != target_color:
            continue

        surface.set_at((cx, cy), new_color)

        queue.append((cx+1, cy))
        queue.append((cx-1, cy))
        queue.append((cx, cy+1))
        queue.append((cx, cy-1))