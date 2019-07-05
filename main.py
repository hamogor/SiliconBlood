from constants import *
import sys
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        player_x, player_y = (0, 0)

        while True:
            events_list = pygame.event.get()#
            self.surface.fill(BGCOLOR)
            self.draw_map()

            for event in events_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in MOVE_N:
                        player_y -= 1
                    elif event.key in MOVE_S:
                        player_y += 1
                    elif event.key in MOVE_W:
                        player_x -= 1
                    elif event.key in MOVE_E:
                        player_x += 1

                    print(player_x)
                    print(player_y)

            self.surface.blit(S_PLAYER, (player_x * TILESIZE, player_y * TILESIZE))

            pygame.display.flip()

    def draw_map(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.surface, LIGHTGREY, (0, y), (WIDTH, y))


if __name__ == '__main__':
    Main().run()
