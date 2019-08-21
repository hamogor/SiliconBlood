import pygame
pygame.init()
TITLE = "Silicon Blood"

GRIDWIDTH, GRIDHEIGHT = 48, 48
CAM_HEIGHT, CAM_WIDTH = 24, 24
TILESIZE = 32

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

FOV_RADIUS = 10
FOV_LIGHT_WALLS = True
FOV_ALGORITHM = 0

FPS = 60

PLAYER_SPEED = 100

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (120, 120, 120)
BLUE = (0, 0, 255)

S_PLAYER = pygame.image.load("assets/player.png")
S_ENEMY = pygame.image.load("assets/Enemy.png")

MOVE_N = (pygame.K_KP8, pygame.K_k, pygame.K_UP)
MOVE_S = (pygame.K_KP2, pygame.K_j, pygame.K_DOWN)
MOVE_W = (pygame.K_KP4, pygame.K_h, pygame.K_LEFT)
MOVE_E = (pygame.K_KP6, pygame.K_l, pygame.K_RIGHT)
MOVE_NW = (pygame.K_KP7, pygame.K_y)
MOVE_NE = (pygame.K_KP9, pygame.K_u)
MOVE_SW = (pygame.K_KP1, pygame.K_b)
MOVE_SE = (pygame.K_KP3, pygame.K_n)
TAKE_STAIRS = pygame.K_COMMA
QUIT = pygame.K_ESCAPE

S_WALL = pygame.image.load("assets/wall.png"), pygame.image.load("assets/dark_wall.png")
S_FLOOR = pygame.image.load("assets/new_floor.png"),  pygame.image.load("assets/new_floor_dark.png")
S_FOG = pygame.image.load("assets/fow.png")
S_STAIRS = pygame.image.load("assets/stairs.png"), pygame.image.load("assets/dark_stairs.png")
