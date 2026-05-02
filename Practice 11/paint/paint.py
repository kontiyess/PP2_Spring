import pygame
import math

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (180, 180, 180)

screen.fill(WHITE)

tool = "draw"
color = BLACK

drawing = False
start_pos = (0, 0)
last_pos = None

font = pygame.font.SysFont(None, 22)

buttons = {
    "rect": pygame.Rect(10, 10, 90, 30),
    "square": pygame.Rect(110, 10, 90, 30),
    "circle": pygame.Rect(210, 10, 90, 30),
    "triangle_r": pygame.Rect(310, 10, 90, 30),
    "triangle_e": pygame.Rect(410, 10, 90, 30),
    "rhombus": pygame.Rect(510, 10, 90, 30),

    "draw": pygame.Rect(10, 50, 90, 30),
    "eraser": pygame.Rect(110, 50, 90, 30),
}

colors = {
    "black": pygame.Rect(10, 90, 30, 30),
    "red": pygame.Rect(50, 90, 30, 30),
    "green": pygame.Rect(90, 90, 30, 30),
    "blue": pygame.Rect(130, 90, 30, 30),
}


def draw_ui():
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, 130))

    for name, rect in buttons.items():
        if tool == name:
            pygame.draw.rect(screen, DARK_GRAY, rect)
        else:
            pygame.draw.rect(screen, GRAY, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 7))

    for cname, rect in colors.items():
        col = BLACK if cname == "black" else RED if cname == "red" else GREEN if cname == "green" else BLUE
        pygame.draw.rect(screen, col, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            for name, rect in buttons.items():
                if rect.collidepoint(mx, my):
                    tool = name

            if colors["black"].collidepoint(mx, my):
                color = BLACK
            if colors["red"].collidepoint(mx, my):
                color = RED
            if colors["green"].collidepoint(mx, my):
                color = GREEN
            if colors["blue"].collidepoint(mx, my):
                color = BLUE

            if my > 130:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                end_pos = event.pos
                last_pos = None

                x1, y1 = start_pos
                x2, y2 = end_pos

                if tool == "rect":
                    pygame.draw.rect(screen, color, (min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1)), 2)

                elif tool == "square":
                    size = min(abs(x2-x1), abs(y2-y1))
                    pygame.draw.rect(screen, color, (x1, y1, size, size), 2)

                elif tool == "circle":
                    radius = int(math.hypot(x2-x1, y2-y1))
                    pygame.draw.circle(screen, color, start_pos, radius, 2)

                elif tool == "triangle_r":
                    pygame.draw.polygon(screen, color, [(x1,y1), (x2,y2), (x1,y2)], 2)

                elif tool == "triangle_e":
                    side = abs(x2-x1)
                    height = side * math.sqrt(3) / 2
                    pygame.draw.polygon(screen, color, [
                        (x1, y1),
                        (x1 + side, y1),
                        (x1 + side/2, y1 - height)
                    ], 2)

                elif tool == "rhombus":
                    cx = (x1 + x2)//2
                    cy = (y1 + y2)//2
                    pygame.draw.polygon(screen, color, [
                        (cx, y1),
                        (x2, cy),
                        (cx, y2),
                        (x1, cy)
                    ], 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "draw":
                if last_pos:
                    pygame.draw.line(screen, color, last_pos, event.pos, 3)
                last_pos = event.pos

            elif drawing and tool == "eraser":
                if last_pos:
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, 12)
                last_pos = event.pos

    draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()