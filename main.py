from ecs.display.display import DisplaySystem
from ecs.display.display_component import DisplayComponent
from ecs.input.input import InputSystem
from ecs.input.input_component import InputComponent
from ecs.action.action import ActionSystem
from ecs.action.action_component import ActionComponent
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
        self.input_system = InputSystem()
        self.action_system = ActionSystem()
        self.player = Actor(DisplayComponent(5 * TILESIZE, 5 * TILESIZE, S_PLAYER),
                            InputComponent(),
                            ActionComponent())

        self.container = Container()

        self.container.add_system(self.display_system)
        self.container.add_system(self.action_system)
        self.container.add_system(self.input_system)

        self.container.add_entity(self.player)

    def game_loop(self):
        self.container.update()
        while not self.quit:
            self.input_system.update(self.container.entities)
            if self.player.get(InputComponent).input:
                self.action_system.update(self.container.entities)
                self.display_system.update(self.container.entities)

            #if self.



if __name__ == '__main__':
    SiliconBlood().game_loop()
