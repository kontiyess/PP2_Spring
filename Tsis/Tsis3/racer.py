import os
import random
from dataclasses import dataclass, field
from typing import Tuple, Optional

import pygame

from persistence import save_score
from ui import draw_text, Button



# CONFIG
SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 700

ROAD_LEFT  = 60
ROAD_WIDTH = 380
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

LANES  = 4
LANE_W = ROAD_WIDTH // LANES

FPS             = 60
FINISH_DISTANCE = 3000

WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0  )
GRAY    = (90,  90,  90 )
DARK_GRAY = (40, 40, 40 )
GREEN   = (30,  150, 60 )
RED     = (220, 40,  40 )
BLUE    = (40,  120, 230)
YELLOW  = (255, 220, 0  )
ORANGE  = (255, 150, 0  )
PURPLE  = (150, 70,  220)
CYAN    = (0,   220, 220)
BROWN   = (120, 70,  30 )

# Car colour options (for settings)
CAR_COLORS = {
    "blue":   (40,  120, 230),
    "red":    (220, 40,  40 ),
    "green":  (30,  180, 60 ),
    "yellow": (230, 200, 0  ),
    "purple": (150, 70,  220),
}

DIFFICULTY = {
    "easy":   {"speed": 1.5, "traffic": 1.15, "obstacles": 1.35},
    "normal": {"speed": 2.2, "traffic": 1.0,  "obstacles": 1.0 },
    "hard":   {"speed": 3.0, "traffic": 0.75, "obstacles": 0.8 },
}

ASSET_DIR   = os.path.join(os.path.dirname(__file__), "assets")

# =========================
# SOUND
# =========================
def _load_sound(name):
    import os as _os
    path = _os.path.join(ASSET_DIR, name)
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

SND_CRASH = None  # loaded after pygame.mixer init in RacerGame

def _play_snd(s, enabled):
    if enabled and s:
        s.play()

def _start_music(enabled):
    import os as _os
    path = _os.path.join(ASSET_DIR, "music.mp3")
    if enabled and _os.path.exists(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.4)
        except Exception:
            pass

def _stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


def _img(name: str, size: Tuple[int, int]) -> Optional[pygame.Surface]:
    path = os.path.join(ASSET_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, size)
    except Exception:
        return None


def lane_center_x(lane: int) -> int:
    return ROAD_LEFT + lane * LANE_W + LANE_W // 2


# FLOATING TEXT
@dataclass
class FloatingText:
    text:  str
    x:     int
    y:     int
    color: Tuple[int, int, int] = field(default_factory=lambda: WHITE)
    timer: int = 60

    def update(self):
        self.y    -= 1
        self.timer -= 1



# SPRITES
class Player(pygame.sprite.Sprite):
    def __init__(self, car_color: str = "blue"):
        super().__init__()
        base = _img("player.png", (42, 70))
        if base:
            self.image = base
        else:
            self.image = pygame.Surface((42, 70), pygame.SRCALPHA)
            color = CAR_COLORS.get(car_color, BLUE)
            pygame.draw.rect(self.image, color, (6, 6, 30, 58), border_radius=8)

        self.rect  = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 95))
        self.speed = 6
        self.shield = False

    def set_shield(self, val: bool):
        self.shield = val

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and self.rect.left   > ROAD_LEFT:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right  < ROAD_RIGHT:
            self.rect.x += self.speed
        if keys[pygame.K_UP]   and self.rect.top     > 80:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom  < SCREEN_HEIGHT - 20:
            self.rect.y += self.speed


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, speed: float, forbidden: pygame.Rect):
        super().__init__()
        img = _img("enemy.png", (44, 70))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((44, 70))
            self.image.fill(RED)
        self.rect  = self.image.get_rect()
        self.speed = speed
        self._safe_spawn(forbidden)

    def _safe_spawn(self, forbidden: pygame.Rect):
        for _ in range(20):
            lane = random.randint(0, LANES - 1)
            x    = lane_center_x(lane)
            y    = random.randint(-400, -80)
            self.rect.center = (x, y)
            if not self.rect.colliderect(forbidden.inflate(80, 260)):
                return

    def update(self, road_speed: float):
        self.rect.y += int(self.speed + road_speed * 0.4)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, forbidden: pygame.Rect):
        super().__init__()
        self.value = random.choice([1, 2, 3])
        img = _img("coin.png", (22, 22))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (11, 11), 11)
        self.rect = self.image.get_rect()
        self._safe_spawn(forbidden)

    def _safe_spawn(self, forbidden: pygame.Rect):
        for _ in range(20):
            lane = random.randint(0, LANES - 1)
            self.rect.center = (lane_center_x(lane), random.randint(-600, -60))
            if not self.rect.colliderect(forbidden.inflate(60, 220)):
                return

    def update(self, speed: float):
        self.rect.y += int(speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    KINDS = ["barrier", "oil", "bump", "nitro_strip"]

    def __init__(self, kind: str, forbidden: pygame.Rect):
        super().__init__()
        self.kind = kind

        if kind == "barrier":
            img = _img("obstacle.png", (44, 60))
            if img:
                self.image = img
            else:
                self.image = pygame.Surface((44, 60), pygame.SRCALPHA)
                pygame.draw.rect(self.image, BROWN, (0, 0, 44, 60), border_radius=6)
                pygame.draw.line(self.image, RED, (0, 30), (44, 30), 4)

        elif kind == "oil":
            self.image = pygame.Surface((40, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (20, 20, 20), (0, 0, 40, 24))
            pygame.draw.ellipse(self.image, (80, 0, 100, 180), (6, 4, 20, 10))

        elif kind == "bump":
            self.image = pygame.Surface((LANE_W - 4, 14), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (200, 160, 0), (0, 0, LANE_W - 4, 14), border_radius=4)
            for i in range(0, LANE_W - 4, 12):
                pygame.draw.rect(self.image, BLACK, (i, 0, 6, 14))

        elif kind == "nitro_strip":
            self.image = pygame.Surface((LANE_W - 4, 20), pygame.SRCALPHA)
            pygame.draw.rect(self.image, CYAN, (0, 0, LANE_W - 4, 20), border_radius=4)
            mid = (LANE_W - 4) // 2
            pygame.draw.polygon(self.image, YELLOW, [(mid, 2), (mid + 10, 14), (mid + 4, 14), (mid + 4, 18), (mid - 4, 18), (mid - 4, 14), (mid - 10, 14)])

        else:
            self.image = pygame.Surface((44, 44), pygame.SRCALPHA)
            pygame.draw.rect(self.image, PURPLE, (0, 0, 44, 44), border_radius=6)

        self.rect = self.image.get_rect()
        self._safe_spawn(forbidden)

    def _safe_spawn(self, forbidden: pygame.Rect):
        for _ in range(20):
            lane = random.randint(0, LANES - 1)
            self.rect.center = (lane_center_x(lane), random.randint(-700, -80))
            if not self.rect.colliderect(forbidden.inflate(80, 260)):
                return

    def update(self, speed: float):
        self.rect.y += int(speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    _IMGS = {"nitro": ("nitro.png",  (40, 40), ORANGE),
             "shield":("shield.png", (40, 40), CYAN  ),
             "repair":("repair.png", (40, 40), PURPLE)}

    def __init__(self, kind: str, forbidden: pygame.Rect):
        super().__init__()
        self.kind  = kind
        self.timer = 360

        fname, size, fallback = self._IMGS[kind]
        img = _img(fname, size)
        if img:
            self.image = img
        else:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.circle(self.image, fallback, (size[0]//2, size[1]//2), size[0]//2)

        self.rect = self.image.get_rect()
        self._safe_spawn(forbidden)

    def _safe_spawn(self, forbidden: pygame.Rect):
        for _ in range(20):
            lane = random.randint(0, LANES - 1)
            self.rect.center = (lane_center_x(lane), random.randint(-900, -120))
            if not self.rect.colliderect(forbidden.inflate(80, 260)):
                return

    def update(self, speed: float):
        self.rect.y  += int(speed)
        self.timer   -= 1
        if self.rect.top > SCREEN_HEIGHT or self.timer <= 0:
            self.kill()


# GAME OVER / FINISH SCREEN
def result_screen(screen: pygame.Surface, title: str,
                  score: int, distance: int, coins: int,
                  font: pygame.font.Font, big_font: pygame.font.Font) -> str:
    """Returns 'retry', 'menu', or 'quit'."""
    clock = pygame.time.Clock()

    btn_retry = Button(100, 490, 130, 50, "Retry")
    btn_menu  = Button(270, 490, 130, 50, "Main Menu")

    title_color = RED if title == "GAME OVER" else YELLOW

    while True:
        clock.tick(60)
        screen.fill((20, 20, 30))

        draw_text(screen, title, big_font, title_color, SCREEN_WIDTH // 2, 120, center=True)

        lines = [
            f"Score:    {score}",
            f"Distance: {distance} m",
            f"Coins:    {coins}",
        ]
        y = 220
        for line in lines:
            draw_text(screen, line, font, WHITE, SCREEN_WIDTH // 2, y, center=True)
            y += 45

        btn_retry.draw(screen, font)
        btn_menu.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if btn_retry.clicked(event):
                return "retry"
            if btn_menu.clicked(event):
                return "menu"


# MAIN GAME
class RacerGame:
    def __init__(self, screen: pygame.Surface, settings: dict, username: str):
        self.screen   = screen
        self.settings = settings
        self.username = username

        self.clock    = pygame.time.Clock()
        self.font     = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 42, bold=True)

        self.car_color = settings.get("car_color", "blue")
        self.player    = Player(self.car_color)

        self._sound = settings.get("sound", True)
        global SND_CRASH
        SND_CRASH = _load_sound("crash.mp3")
        _start_music(self._sound)

        diff = DIFFICULTY[settings.get("difficulty", "normal")]
        self.base_speed      = diff["speed"]
        self.traffic_factor  = diff["traffic"]
        self.obstacle_factor = diff["obstacles"]

        # sprite groups
        self.traffic   = pygame.sprite.Group()
        self.coins     = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups  = pygame.sprite.Group()

        self.floating: list[FloatingText] = []

        # stats
        self.score            = 0.0
        self.distance         = 0.0
        self.coins_collected  = 0

        # power-up state
        self.active_power: Optional[str] = None
        self.power_timer  = 0

        # road scroll
        self.road_offset = 0

        # road background image
        self.road_bg = _img("road.png", (ROAD_WIDTH, SCREEN_HEIGHT))

    def _draw_road(self):
        self.screen.fill((34, 120, 34))   # grass

        if self.road_bg:
            # scroll the road texture
            speed = int(self.current_speed())
            self.road_offset = (self.road_offset + speed) % SCREEN_HEIGHT
            # draw twice for seamless scroll
            self.screen.blit(self.road_bg, (ROAD_LEFT, self.road_offset - SCREEN_HEIGHT))
            self.screen.blit(self.road_bg, (ROAD_LEFT, self.road_offset))
        else:
            pygame.draw.rect(self.screen, DARK_GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # dashed lane lines
        dash_h = 30
        gap    = 20
        speed  = int(self.current_speed())
        self.road_offset = (self.road_offset + speed) % (dash_h + gap)

        for i in range(1, LANES):
            x = ROAD_LEFT + i * LANE_W
            y = -((self.road_offset) % (dash_h + gap))
            while y < SCREEN_HEIGHT:
                pygame.draw.rect(self.screen, WHITE, (x - 2, y, 4, dash_h))
                y += dash_h + gap

    def _draw_hud(self):
        speed = self.current_speed()

        x = ROAD_LEFT + 5

        draw_text(self.screen, f"Score: {int(self.score)}", self.font, WHITE, x, 10)
        draw_text(self.screen, f"Dist:  {int(self.distance)} m", self.font, WHITE, x, 35)
        draw_text(self.screen, f"Coins: {self.coins_collected}", self.font, WHITE, x, 60)

        remaining = max(0, FINISH_DISTANCE - int(self.distance))
        draw_text(self.screen, f"Finish:   {remaining} m", self.font, YELLOW, 10, 85)

        # active power-up
        if self.active_power:
            if self.active_power == "shield":
                label = "SHIELD active"
                color = CYAN
            elif self.active_power == "nitro":
                secs  = max(0, self.power_timer // FPS)
                label = f"NITRO  {secs}s"
                color = ORANGE
            else:
                label = self.active_power
                color = WHITE
            draw_text(self.screen, label, self.font, color,
                      SCREEN_WIDTH - 5, 10,
                      center=False)

        # shield indicator on player
        if self.player.shield:
            pygame.draw.circle(self.screen, CYAN,
                               self.player.rect.center, 32, 2)

    # ------------------------------------------------------------------ logic
    def current_speed(self) -> float:
        """Speed grows slowly with distance; nitro adds a multiplier."""
        progress = min(self.distance / FINISH_DISTANCE, 1.0)
        speed    = self.base_speed * (1.0 + progress * 0.1)   # up to +10% at finish

        if self.active_power == "nitro":
            speed *= 3.0

        return speed

    def _spawn(self):
        prog = min(self.distance / FINISH_DISTANCE, 1.0)

        # traffic – scales from base rate → 3× at finish
        traffic_rate = 0.018 * (1 + 2 * prog) / self.traffic_factor
        if random.random() < traffic_rate:
            enemy_speed = random.uniform(1.5, 2.5 + prog * 2)
            self.traffic.add(TrafficCar(enemy_speed, self.player.rect))

        # coins — spawn less often
        if random.random() < 0.03:
            self.coins.add(Coin(self.player.rect))

        # obstacles – scales gently
        obs_rate = 0.012 * (1 + prog) / self.obstacle_factor
        if random.random() < obs_rate:
            kind = random.choice(Obstacle.KINDS)
            self.obstacles.add(Obstacle(kind, self.player.rect))

        # power-ups — more frequent so player sees them
        if len(self.powerups) == 0 and random.random() < 0.03:
            kind = random.choice(["nitro", "shield", "repair"])
            self.powerups.add(PowerUp(kind, self.player.rect))

    def _handle_collisions(self) -> bool:
        """Returns True if the player should die."""
        # --- traffic ---
        hit = pygame.sprite.spritecollideany(self.player, self.traffic)
        if hit:
            if self.player.shield:
                self.player.set_shield(False)
                self.active_power = None
                hit.kill()
                self.floating.append(FloatingText("SHIELD USED!", hit.rect.centerx, hit.rect.centery, CYAN))
            else:
                _play_snd(SND_CRASH, self._sound)
                return True   # crash

        # --- obstacles ---
        for ob in pygame.sprite.spritecollide(self.player, self.obstacles, False):
            if ob.kind == "oil":
                self.player.rect.x += random.choice([-44, 44])
                self.player.rect.x  = max(ROAD_LEFT, min(ROAD_RIGHT - 42, self.player.rect.x))
                ob.kill()
            elif ob.kind == "bump":
                self.player.rect.y = min(SCREEN_HEIGHT - 20, self.player.rect.y + 20)
                ob.kill()
            elif ob.kind == "nitro_strip":
                self._collect_powerup("nitro")
                ob.kill()
            else:   # barrier
                if self.player.shield:
                    self.player.set_shield(False)
                    self.active_power = None
                    ob.kill()
                    self.floating.append(FloatingText("SHIELD USED!", ob.rect.centerx, ob.rect.centery, CYAN))
                else:
                    _play_snd(SND_CRASH, self._sound)
                    return True

        # --- coins ---
        for c in pygame.sprite.spritecollide(self.player, self.coins, True):
            self.coins_collected += c.value
            gained = 10 * c.value
            self.score += gained
            self.floating.append(FloatingText(f"+{gained}", c.rect.centerx, c.rect.centery, YELLOW))
            pass  # coin sound

        # --- power-ups ---
        for p in pygame.sprite.spritecollide(self.player, self.powerups, True):
            self._collect_powerup(p.kind, p.rect.center)

        return False

    def _collect_powerup(self, kind: str, pos: Tuple[int,int] = (250, 350)):
        
        if kind == "repair":
            self.player.set_shield(True)
            self.active_power = "shield"
            self.floating.append(FloatingText("REPAIRED!", pos[0], pos[1], PURPLE))
            return

        # only one power-up active at a time
        if self.active_power == "shield":
            self.player.set_shield(False)

        self.active_power = kind
        if kind == "nitro":
            self.power_timer = 4 * FPS          # 4 seconds
            self.floating.append(FloatingText("NITRO!", pos[0], pos[1], ORANGE))
            pass  # nitro sound
        elif kind == "shield":
            self.power_timer = 9999
            self.player.set_shield(True)
            self.floating.append(FloatingText("SHIELD!", pos[0], pos[1], CYAN))
            pass  # shield sound

    def _update_power(self):
        if self.active_power and self.active_power != "shield":
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.active_power = None

    # ------------------------------------------------------------------ main loop
    def run(self) -> str:
        """Returns 'menu', 'retry', or 'quit'."""
        while True:
            self.clock.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit"
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return "menu"

            speed          = self.current_speed()
            self.distance += speed    # ~pixels → metres
            self.score    += 0.05 * speed

            self._spawn()

            self.player.move()
            self.traffic.update(speed)
            self.coins.update(speed)
            self.obstacles.update(speed)
            self.powerups.update(speed)

            crashed = self._handle_collisions()
            self._update_power()

            # ---- finish line ----
            if self.distance >= FINISH_DISTANCE:
                self.score += 500   # finish bonus
                _stop_music()
                pass  # win sound
                save_score(self.username, int(self.score), int(self.distance), self.coins_collected)
                return result_screen(self.screen, "YOU WIN!",
                                     int(self.score), int(self.distance),
                                     self.coins_collected, self.font, self.big_font)

            if crashed:
                _stop_music()
                save_score(self.username, int(self.score), int(self.distance), self.coins_collected)
                return result_screen(self.screen, "GAME OVER",
                                     int(self.score), int(self.distance),
                                     self.coins_collected, self.font, self.big_font)

            # ---- draw ----
            self._draw_road()

            self.traffic.draw(self.screen)
            self.coins.draw(self.screen)
            self.obstacles.draw(self.screen)
            self.powerups.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)

            for ft in self.floating[:]:
                draw_text(self.screen, ft.text, self.font, ft.color, ft.x, ft.y, center=True)
                ft.update()
                if ft.timer <= 0:
                    self.floating.remove(ft)

            self._draw_hud()
            pygame.display.flip()