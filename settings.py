import pygame
pygame.init()

TITLE = "Silicon Blood"

# game settings
#WIDTH = pygame.display.Info().current_w # 16 * 64 or 32 * 32 or 64 * 16
#HEIGHT = pygame.display.Info().current_h  # 16 * 48 or 32 * 24 or 64 * 12

WIDTH, HEIGHT = 1920, 1080

FPS = 60

# Sprite size
TILESIZE = 32

# Full map size
GRIDWIDTH, GRIDHEIGHT = 64,64


# Camera size
CAM_WIDTH = 32
CAM_HEIGHT = 32

# Keybinds
MOVE_N = (pygame.K_KP8, pygame.K_k, pygame.K_UP)
MOVE_S = (pygame.K_KP2, pygame.K_j, pygame.K_DOWN)
MOVE_W = (pygame.K_KP4, pygame.K_h, pygame.K_LEFT)
MOVE_E = (pygame.K_KP6, pygame.K_l, pygame.K_RIGHT)
MOVE_NW = (pygame.K_KP7, pygame.K_y)
MOVE_NE = (pygame.K_KP9, pygame.K_u)
MOVE_SW = (pygame.K_KP1, pygame.K_b)
MOVE_SE = (pygame.K_KP3, pygame.K_n)
TAKE_STAIRS = (pygame.K_COMMA)
QUIT = pygame.K_ESCAPE

# Load assets
S_PLAYER = pygame.image.load("assets/player.png")
S_WALL = pygame.image.load("assets/wall.png")
S_FLOOR = pygame.image.load("assets/floor.png")
S_DWALL = pygame.image.load("assets/dark_wall.png")
S_DFLOOR = pygame.image.load("assets/dark_floor.png")
S_ENEMY = pygame.image.load("assets/Enemy.png")
S_FOG = pygame.image.load("assets/fow.png")
S_STAIRS = pygame.image.load("assets/stairs.png")
S_DSTAIRS = pygame.image.load("assets/dark_stairs.png")
S_TELEPORTER = pygame.image.load("assets/teleporter_spritesheet.png")

S_DUNGEON_FLOOR = {"floor": pygame.image.load("assets/dungeon_floor/floor.png"),
                   "floor_bottom": pygame.image.load("assets/dungeon_floor/floor_bottom.png"),
                   "floor_bottom_left": pygame.image.load("assets/dungeon_floor/floor_bottom_left.png"),
                   "floor_bottom_right": pygame.image.load("assets/dungeon_floor/floor_bottom_right.png"),
                   "floor_left": pygame.image.load("assets/dungeon_floor/floor_left.png"),
                   "floor_right": pygame.image.load("assets/dungeon_floor/floor_right.png"),
                   "floor_top": pygame.image.load("assets/dungeon_floor/floor_top.png"),
                   "floor_top_left": pygame.image.load("assets/dungeon_floor/floor_top_left.png"),
                   "floor_top_right": pygame.image.load("assets/dungeon_floor/floor_top_right.png")}

LIGHTGREY = (100, 100, 100)

# Fov settings
FOV_RADIUS = 10
FOV_LIGHT_WALLS = True
FOV_ALGORITHM = 0

PLAYER_SPEED = 100
