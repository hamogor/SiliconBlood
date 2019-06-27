# 3rd party modules
import pygame
from random import randint
# game files
import constants


#      _______.___________..______       __    __    ______ .___________.
#     /       |           ||   _  \     |  |  |  |  /      ||           |
#    |   (----`---|  |----`|  |_)  |    |  |  |  | |  ,----'`---|  |----`
#     \   \       |  |     |      /     |  |  |  | |  |         |  |
# .----)   |      |  |     |  |\  \----.|  `--'  | |  `----.    |  |
# |_______/       |__|     | _| `._____| \______/   \______|    |__|

class StrucTile:
    def __init__(self, block_path):
        self.block_path = block_path


class ObjActor:
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x  # map address
        self.y = y  # map address
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def move(self, dx, dy):
        if not GAME_MAP[self.x + dx][self.y + dy].block_path:
            self.x += dx
            self.y += dy


class ComCreature:
    def __init__(self, name_instance, hp=10):
        self.name_instance = name_instance
        self.hp = hp


class ComAi:
    def take_turn(self):
        self.owner.move(randint(-1, 1), randint(-1, 1))


def map_create():
    new_map = [[StrucTile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map


def draw_game():

    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    draw_map(GAME_MAP)

    for obj in GAME_OBJECTS:
        obj.draw()

    pygame.display.flip()


def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path:
                # draw wall
                SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            else:
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def game_main_loop():
    game_quit = False

    while not game_quit:

        # handle player input
        player_action = game_handle_keys()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no-action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


def game_initialize():
    '''This function initializes the main window, and pygame'''

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))

    GAME_MAP = map_create()

    creature_com1 = ComCreature("greg")
    PLAYER = ObjActor(0, 0, "python", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = ComCreature("WigWig")
    ai_com = ComAi()
    ENEMY = ObjActor(15, 15, "WigWig", constants.S_WIGWIG, ai=ai_com)

    GAME_OBJECTS = [PLAYER, ENEMY]


def game_handle_keys():
    # get player input
    events_list = pygame.event.get()

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.move(0, -1)
                return "player-moved"

            if event.key == pygame.K_DOWN:
                PLAYER.move(0, 1)
                return "player-moved"

            if event.key == pygame.K_LEFT:
                PLAYER.move(-1, 0)
                return "player-moved"

            if event.key == pygame.K_RIGHT:
                PLAYER.move(1, 0)
                return "player-moved"

    return "no-action"


if __name__ == '__main__':
    game_initialize()
    game_main_loop()