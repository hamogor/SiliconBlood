import pygame

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Silicon Blood"

TILESIZE = 32

GRIDWIDTH = 100
GRIDHEIGHT = 100

CAM_WIDTH = 32
CAM_HEIGHT = 32

MOVE_N = (pygame.K_KP8, pygame.K_k, pygame.K_UP)
MOVE_S = (pygame.K_KP2, pygame.K_j, pygame.K_DOWN)
MOVE_W = (pygame.K_KP4, pygame.K_h, pygame.K_LEFT)
MOVE_E = (pygame.K_KP6, pygame.K_l, pygame.K_RIGHT)
MOVE_NW = (pygame.K_KP7, pygame.K_y)
MOVE_NE = (pygame.K_KP9, pygame.K_u)
MOVE_SW = (pygame.K_KP1, pygame.K_b)
MOVE_SE = (pygame.K_KP3, pygame.K_n)
QUIT = (pygame.K_ESCAPE)

S_PLAYER = pygame.image.load("assets/player.png")
S_WALL = pygame.image.load("assets/wall.png")
S_FLOOR = pygame.image.load("assets/floor.png")
S_DWALL = pygame.image.load("assets/dark_wall.png")
S_DFLOOR = pygame.image.load("assets/dark_floor.png")
S_ENEMY = pygame.image.load("assets/Enemy.png")
S_FOG = pygame.image.load("assets/fow.png")
LIGHTGREY = (100, 100, 100)

FOV_RADIUS = 10
FOV_LIGHT_WALLS = True
FOV_ALGORITHM = 0

#if key_pressed in MOVE_N:
#    dc.y -= 1
#elif key_pressed in MOVE_S:
#    dc.y += 1
#elif key_pressed in MOVE_W:
#    dc.x -= 1
#elif key_pressed in MOVE_E:
#    dc.x += 1
