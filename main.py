from ecs.display.display import DisplaySystem
from ecs.display.display_component import DisplayComponent
from ecs.input.input import InputSystem
from ecs.input.input_component import InputComponent
from ecs.action.action import ActionSystem
from ecs.action.action_component import ActionComponent
from ecs.level.level import LevelSystem
from ecs.fov.fov import FovSystem
from ecs.fov.fov_component import FovComponent
from ecs.camera.camera_component import CameraComponent
from ecs.container import Container
from settings import *
from structs.actor import Actor
import pygame


class SiliconBlood:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(S_PLAYER)
        pygame.key.set_repeat(200, 100)
        self.clock = pygame.time.Clock()
        self.quit = False

        self.level_system = LevelSystem()

        self.input_system = InputSystem()
        self.display_system = DisplaySystem(self.level_system.level)
        self.fov_system = FovSystem(self.level_system.level)

        self.action_system = ActionSystem(self.level_system.level)

        self.player = Actor(DisplayComponent(5, 5, S_PLAYER),
                            InputComponent(),
                            ActionComponent(),
                            CameraComponent(0, 0),
                            FovComponent())

        self.container = Container()
        self.container.add_system(self.level_system)
        self.container.add_system(self.fov_system)
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
                self.fov_system.update(self.container.entities)
                self.display_system.update(self.container.entities)
                self.level_system.update(self.container.entities)

            if self.player.get(ActionComponent).action == "quit":
                self.quit = True

            #self.clock.tick(FPS)


if __name__ == '__main__':
    SiliconBlood().game_loop()
