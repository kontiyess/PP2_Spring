import pygame
from persistence import load_leaderboard, load_settings, save_settings
from racer import RacerGame, CAR_COLORS
from ui import Button, draw_text

pygame.init()
pygame.display.set_caption("RACER")

SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock  = pygame.time.Clock()

font     = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 48, bold=True)

WHITE = (255, 255, 255)
BLACK = (0,   0,   0  )
GRAY  = (235, 235, 235)
RED   = (220, 40,  40 )

settings = load_settings()
username = "Player"


# =========================
# USERNAME INPUT
# =========================
def get_username():
    name = ""
    while True:
        clock.tick(60)
        screen.fill(GRAY)

        draw_text(screen, "Enter your name", big_font, BLACK, SCREEN_WIDTH // 2, 180, center=True)
        draw_text(screen, name + "|",         font,     BLACK, SCREEN_WIDTH // 2, 260, center=True)
        draw_text(screen, "Enter = start  |  ESC = back",
                  font, BLACK, SCREEN_WIDTH // 2, 320, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() or "Player"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode


# =========================
# MAIN MENU
# =========================
def main_menu():
    buttons = {
        "play":        Button(140, 220, 220, 50, "Play"),
        "leaderboard": Button(140, 290, 220, 50, "Leaderboard"),
        "settings":    Button(140, 360, 220, 50, "Settings"),
        "quit":        Button(140, 430, 220, 50, "Quit"),
    }

    while True:
        clock.tick(60)
        screen.fill(GRAY)

        draw_text(screen, "RACER", big_font, RED, SCREEN_WIDTH // 2, 120, center=True)

        for button in buttons.values():
            button.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for state, button in buttons.items():
                if button.clicked(event):
                    return state


# =========================
# LEADERBOARD
# =========================
def leaderboard_screen():
    back_button = Button(140, 620, 220, 50, "Back")
    header_font = pygame.font.SysFont("Arial", 18, bold=True)
    row_font    = pygame.font.SysFont("Arial", 17)

    while True:
        clock.tick(60)
        screen.fill(GRAY)

        draw_text(screen, "Leaderboard", big_font, BLACK, SCREEN_WIDTH // 2, 65, center=True)

        # header
        draw_text(screen, "#   Name          Score    Dist   Coins",
                  header_font, BLACK, 20, 120)
        pygame.draw.line(screen, BLACK, (20, 140), (SCREEN_WIDTH - 20, 140), 2)

        leaderboard = load_leaderboard()
        y = 150
        for i, entry in enumerate(leaderboard[:10], start=1):
            name  = entry.get("name",     "?")[:10]
            score = entry.get("score",    0)
            dist  = entry.get("distance", 0)
            coins = entry.get("coins",    0)
            line  = f"{i:<3} {name:<13} {score:<8} {int(dist):<6} {coins}"
            color = RED if i == 1 else BLACK
            draw_text(screen, line, row_font, color, 20, y)
            y += 30

        back_button.draw(screen, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back_button.clicked(event):
                return "menu"


# =========================
# SETTINGS
# =========================
def settings_screen():
    global settings

    sound_btn      = Button(140, 200, 220, 50, "")
    difficulty_btn = Button(140, 270, 220, 50, "")
    color_btn      = Button(140, 340, 220, 50, "")
    back_btn       = Button(140, 500, 220, 50, "Back")

    diff_options  = ["easy", "normal", "hard"]
    color_options = list(CAR_COLORS.keys())

    while True:
        clock.tick(60)
        screen.fill(GRAY)

        draw_text(screen, "Settings", big_font, BLACK, SCREEN_WIDTH // 2, 100, center=True)

        sound_btn.text      = f"Sound: {'ON' if settings.get('sound', True) else 'OFF'}"
        difficulty_btn.text = f"Difficulty: {settings.get('difficulty', 'normal')}"
        car_color           = settings.get("car_color", "blue")
        color_btn.text      = f"Car Color: {car_color}"

        sound_btn.draw(screen, font)
        difficulty_btn.draw(screen, font)
        color_btn.draw(screen, font)

        # small colour preview square
        preview_color = CAR_COLORS.get(car_color, (40, 120, 230))
        pygame.draw.rect(screen, preview_color,
                         pygame.Rect(color_btn.rect.right + 10,
                                     color_btn.rect.top + 10,
                                     30, 30), border_radius=6)

        back_btn.draw(screen, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if sound_btn.clicked(event):
                settings["sound"] = not settings.get("sound", True)
                save_settings(settings)

            if difficulty_btn.clicked(event):
                idx = diff_options.index(settings.get("difficulty", "normal"))
                settings["difficulty"] = diff_options[(idx + 1) % len(diff_options)]
                save_settings(settings)

            if color_btn.clicked(event):
                idx = color_options.index(settings.get("car_color", "blue"))
                settings["car_color"] = color_options[(idx + 1) % len(color_options)]
                save_settings(settings)

            if back_btn.clicked(event):
                return "menu"


# =========================
# MAIN LOOP
# =========================
def main():
    global username, settings
    state = "menu"

    while state != "quit":

        if state == "menu":
            state = main_menu()

        elif state == "play":
            name = get_username()
            if name == "quit":
                break
            if name == "menu":
                state = "menu"
            else:
                username = name
                settings = load_settings()          # reload in case settings changed
                game     = RacerGame(screen, settings, username)
                state    = game.run()               # returns 'menu'/'retry'/'quit'

        elif state == "retry":
            # restart with same username
            settings = load_settings()
            game     = RacerGame(screen, settings, username)
            state    = game.run()

        elif state == "leaderboard":
            state = leaderboard_screen()

        elif state == "settings":
            state = settings_screen()

    pygame.quit()


if __name__ == "__main__":
    main()