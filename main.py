from ecs.display.display import DisplaySystem
from ecs.container import Container
from settings import *
from structs.actor import Actor
import pygame


class SiliconBlood:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(S_PLAYER)
        self.clock = pygame.time.Clock()
        self.quit = False

        self.display_system = DisplaySystem()
        self.player = Actor(32, 32, S_PLAYER)

        self.container = Container()

        self.container.add_system(self.display_system)
        self.container.add_entity(self.player)

    def game_loop(self):
        while not self.quit:
            self.clock.tick(FPS)
            self.container.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True


if __name__ == '__main__':
    SiliconBlood().game_loop()
