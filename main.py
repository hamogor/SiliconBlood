# 3rd party modules
import pygame

# game files
import constants


class StrucTile:
    def __init__(self, block_path):
        self.block_path = block_path


class ObjActor:
    """Our basic actor object."""

    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH,
                                        self.y*constants.CELL_HEIGHT))

    def move(self, dx, dy):
        if not GAME_MAP[self.x + dx][self.y + dy].block_path:
            self.x += dx
            self.y += dy


def map_create():
    new_map = [[StrucTile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map


def draw_game():
    global SURFACE_MAIN

    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME_MAP)

    # draw the character
    PLAYER.draw()

    # update the display
    pygame.display.flip()


def draw_map(map_to_draw):

    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path: # if True there is a wall here
                # draw wall
                SURFACE_MAIN.blit(constants.S_WALL, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
            else:
                # draw floor
                SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))


def game_main_loop():
    """In this function we loop the main game."""
    game_quit = False

    while not game_quit:

        # get player input
        events_list = pygame.event.get()

        # process input
        for event in events_list:  # loop through all events that have happened
            if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
                game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)
        # draw the game
        draw_game()

    pygame.quit()
    exit()


def game_initialize():
    """This function initializes the main window, and pygame"""

    global SURFACE_MAIN, GAME_MAP, PLAYER
    # initialize pygame
    pygame.init()

    # set sufrace dimensions
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    # Ideally the surface should be resizable -- we are going to skip this for now

    GAME_MAP = map_create()  # Create the game map. Fills the 2D array with values.

    PLAYER = ObjActor(int(constants.MAP_WIDTH / 2), int(constants.MAP_HEIGHT / 2), constants.S_PLAYER)


if __name__ == '__main__':
    game_initialize()
    print(GAME_MAP)
    game_main_loop()
