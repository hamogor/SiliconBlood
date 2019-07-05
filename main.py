from constants import *
import sys
import pygame


class Main:
    def run(self):
        pygame.init()
        surface = pygame.display.set_mode((WIDTH, HEIGHT))
        player_x, player_y = (0, 0)

        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

        while True:
            events_list = pygame.event.get()

            # process input3
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

            pygame.display.flip()


if __name__ == '__main__':
    Main().run()
