import pygame
import math
from collections import deque
from datetime import datetime
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
TOOLBAR_H = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint TSIS2")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)
text_font = pygame.font.SysFont(None, 28)

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0  )
GRAY   = (200, 200, 200)

PALETTE = [
    BLACK,
    (255, 255, 255),
    (255, 0,   0  ),
    (0,   200, 0  ),
    (0,   0,   255),
    (255, 165, 0  ),
    (255, 255, 0  ),
    (128, 0,   128),
    (0,   200, 200),
    (255, 105, 180),
    (139, 69,  19 ),
    (128, 128, 128),
]

TOOLS = [
    "draw", "line", "rect", "circle",
    "square", "tri_r", "tri_e", "rhomb",
    "fill", "text", "eraser",
]

BRUSH_SIZES = [2, 5, 10]

tool  = "draw"
color = BLACK
size  = 5

drawing = False
start   = None
last    = None

text_mode = False
text      = ""
text_pos  = (0, 0)


# ─────────────────────────── flood fill ───────────────────────────
def flood_fill(surface, x, y, new_color):
    target = surface.get_at((x, y))[:3]
    nc     = new_color[:3] if len(new_color) > 3 else new_color
    if target == nc:
        return

    q       = deque([(x, y)])
    visited = set()

    while q:
        px, py = q.popleft()
        if (px, py) in visited:
            continue
        if px < 0 or px >= WIDTH or py < TOOLBAR_H or py >= HEIGHT:
            continue
        if surface.get_at((px, py))[:3] != target:
            continue

        surface.set_at((px, py), new_color)
        visited.add((px, py))
        q.extend([(px+1, py), (px-1, py), (px, py+1), (px, py-1)])


# ─────────────────────────── shape drawing ────────────────────────
def draw_shape(surface, t, s, e):
    x1, y1 = s
    x2, y2 = e

    if t == "line":
        pygame.draw.line(surface, color, s, e, size)

    elif t == "rect":
        pygame.draw.rect(surface, color,
                         (min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1)), size)

    elif t == "circle":
        r = int(math.hypot(x2-x1, y2-y1))
        pygame.draw.circle(surface, color, s, r, size)

    elif t == "square":
        side = max(abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(surface, color, (x1, y1, side, side), size)

    elif t == "tri_r":
        pygame.draw.polygon(surface, color, [(x1,y1),(x2,y2),(x1,y2)], size)

    elif t == "tri_e":
        side = abs(x2-x1)
        h    = side * math.sqrt(3) / 2
        pygame.draw.polygon(surface, color,
                            [(x1,y1),(x1+side,y1),(x1+side/2, y1-h)], size)

    elif t == "rhomb":
        cx, cy = (x1+x2)//2, (y1+y2)//2
        pygame.draw.polygon(surface, color,
                            [(cx,y1),(x2,cy),(cx,y2),(x1,cy)], size)


# ─────────────────────────── UI ───────────────────────────────────
TOOL_COLS = 6   # tools per row

def tool_rect(i):
    col = i % TOOL_COLS
    row = i // TOOL_COLS
    return pygame.Rect(10 + col * 70, 5 + row * 30, 65, 26)

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_H))

    # tools
    for i, t in enumerate(TOOLS):
        r   = tool_rect(i)
        bg  = (160, 160, 160) if t == tool else (190, 190, 190)
        pygame.draw.rect(screen, bg, r, border_radius=4)
        txt = font.render(t, True, BLACK)
        screen.blit(txt, (r.x + 4, r.y + 6))
        if t == tool:
            pygame.draw.rect(screen, (255, 180, 0), r, 2, border_radius=4)

    # palette (right side)
    pal_x = WIDTH - len(PALETTE) * 26 - 10
    for i, c in enumerate(PALETTE):
        r = pygame.Rect(pal_x + i*26, 62, 24, 24)
        pygame.draw.rect(screen, c, r, border_radius=3)
        pygame.draw.rect(screen, BLACK, r, 1, border_radius=3)
        if c == color:
            pygame.draw.rect(screen, (255, 180, 0), r, 2, border_radius=3)

    # brush sizes  (1 / 2 / 3)
    for i, s in enumerate(BRUSH_SIZES):
        r   = pygame.Rect(10 + i*52, 62, 46, 26)
        bg  = (160, 160, 160) if s == size else (190, 190, 190)
        pygame.draw.rect(screen, bg, r, border_radius=4)
        label = font.render(f"{i+1}: {s}px", True, BLACK)
        screen.blit(label, (r.x + 5, r.y + 5))
        if s == size:
            pygame.draw.rect(screen, (255, 180, 0), r, 2, border_radius=4)

    # current colour preview
    preview = pygame.Rect(WIDTH - 60, 5, 50, 22)
    pygame.draw.rect(screen, color, preview, border_radius=4)
    pygame.draw.rect(screen, BLACK, preview, 1, border_radius=4)

    # hint
    hint = font.render("Ctrl+S = save   1/2/3 = brush size", True, (80, 80, 80))
    screen.blit(hint, (175, 68))


# ─────────────────────────── main loop ────────────────────────────
running = True
while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # ── keyboard ──
        if e.type == pygame.KEYDOWN:

            mods = pygame.key.get_mods()

            # Ctrl+S  (also Cmd+S on macOS)
            if e.key == pygame.K_s and (mods & pygame.KMOD_CTRL or mods & pygame.KMOD_META):
                name = datetime.now().strftime("canvas_%Y%m%d_%H%M%S.png")
                path = os.path.join(os.path.dirname(__file__), name)
                # save only the drawing area (below toolbar)
                drawing_area = canvas.subsurface((0, TOOLBAR_H, WIDTH, HEIGHT - TOOLBAR_H))
                pygame.image.save(drawing_area, path)
                print("Saved:", path)

            # brush size shortcuts
            if not text_mode:
                if e.key == pygame.K_1:
                    size = BRUSH_SIZES[0]
                elif e.key == pygame.K_2:
                    size = BRUSH_SIZES[1]
                elif e.key == pygame.K_3:
                    size = BRUSH_SIZES[2]

                # Escape cancels current drawing
                elif e.key == pygame.K_ESCAPE:
                    drawing = False

            # text input
            if text_mode:
                if e.key == pygame.K_RETURN:
                    img = text_font.render(text, True, color)
                    canvas.blit(img, text_pos)
                    text_mode = False
                    text      = ""
                elif e.key == pygame.K_ESCAPE:
                    text_mode = False
                    text      = ""
                elif e.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += e.unicode

        # ── mouse down ──
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos

            if y < TOOLBAR_H:
                # tool buttons
                for i, t in enumerate(TOOLS):
                    if tool_rect(i).collidepoint(x, y):
                        tool = t

                # palette
                pal_x = WIDTH - len(PALETTE) * 26 - 10
                for i, c in enumerate(PALETTE):
                    if pygame.Rect(pal_x + i*26, 62, 24, 24).collidepoint(x, y):
                        color = c

                # brush sizes
                for i, s in enumerate(BRUSH_SIZES):
                    if pygame.Rect(10 + i*52, 62, 46, 26).collidepoint(x, y):
                        size = s

            else:   # canvas area
                if tool == "fill":
                    flood_fill(canvas, x, y, color)

                elif tool == "text":
                    text_mode = True
                    text      = ""
                    text_pos  = (x, y)

                else:
                    drawing = True
                    start   = (x, y)
                    last    = (x, y)

        # ── mouse move ──
        if e.type == pygame.MOUSEMOTION and drawing:
            if tool == "draw":
                pygame.draw.line(canvas, color, last, e.pos, size)
                last = e.pos
            elif tool == "eraser":
                pygame.draw.line(canvas, WHITE, last, e.pos, size * 3)
                last = e.pos

        # ── mouse up ──
        if e.type == pygame.MOUSEBUTTONUP and drawing:
            if tool not in ("draw", "eraser"):
                draw_shape(canvas, tool, start, e.pos)
            drawing = False

    # ── render ──
    screen.blit(canvas, (0, 0))

    # live preview while dragging shapes
    if drawing and tool not in ("draw", "eraser"):
        temp = canvas.copy()
        draw_shape(temp, tool, start, pygame.mouse.get_pos())
        screen.blit(temp, (0, 0))

    # text cursor preview
    if text_mode:
        img = text_font.render(text + "|", True, color)
        screen.blit(img, text_pos)

    draw_ui()
    pygame.display.flip()

pygame.quit()