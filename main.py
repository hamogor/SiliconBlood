from constants import *
from ecs.display_component import DisplayComponent
from display.display import DisplaySystem
from ecs.entity import Entity
from ecs.container import Container
import sys
import pygame


class Player(Entity):
    def __init__(self):
        super().__init__(DisplayComponent(S_PLAYER, 0, 0))


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.player = Player()
        self.container = Container()

        self.container.add_system(DisplaySystem())

        self.container.add_entity(self.player)


    def game_loop(self):
        self.container.update()

        while True:
            events_list = pygame.event.get()
            for event in events_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #if event.type == pygame.KEYDOWN:
                #    if event.key in MOVE_N:
                #        player_y -= 1
                #    elif event.key in MOVE_S:
                #        player_y += 1
                #    elif event.key in MOVE_W:
                #        player_x -= 1
                #    elif event.key in MOVE_E:
                #        player_x += 1
                #    elif event.key in MOVE_NW:
                #        player_x -= 1
                #        player_y -= 1
                #    elif event.key in MOVE_NE:
                #        player_x += 1
                #        player_y -= 1
                #    elif event.key in MOVE_SW:
                #        player_x -= 1
                #        player_y += 1
                #    elif event.key in MOVE_SE:
                #        player_x += 1
                #        player_y += 1

            self.surface.blit(S_PLAYER, (0 * TILESIZE, 0 * TILESIZE))

            pygame.display.flip()

    def draw_map(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.surface, LIGHTGREY, (0, y), (WIDTH, y))


if __name__ == '__main__':
    Main().run()
