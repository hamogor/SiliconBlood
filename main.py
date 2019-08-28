from ecs.display.display import DisplaySystem
from ecs.display.display_component import DisplayComponent
from ecs.action.action import ActionSystem
from ecs.action.action_component import ActionComponent
from structs.actor import Actor
from structs.player import Player
from ecs.input.input import InputSystem
from ecs.input.input_component import InputComponent
from ecs.level.level import LevelSystem
from ecs.camera.camera import CameraSystem
from ecs.camera.camera_component import CameraComponent
from ecs.fov.fov import FovSystem
from ecs.fov.fov_component import FovComponent
from ecs.ai.ai import AiSystem
from structs.game_states import GameStates
from settings import *
from ecs.container import Container
import pygame


class SiliconBlood:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(S_PLAYER)
        pygame.key.set_repeat(200, 40)

        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.quit = False

        self.level_system = LevelSystem(1)
        self.camera_system = CameraSystem()
        self.fov_system = FovSystem(self.level_system.level)
        self.display_system = DisplaySystem(self.display, self.camera_system, self.level_system.level)
        self.action_system = ActionSystem(self.level_system.level)
        self.ai_system = AiSystem(self.level_system.level)
        self.input_system = InputSystem()
        self.player = Player(DisplayComponent(S_PLAYER,
                                              self.level_system.map.spawn[0],
                                              self.level_system.map.spawn[1],
                                              alpha=True),
                             ActionComponent(),
                             InputComponent(),
                             CameraComponent(),
                             FovComponent(self.fov_system.fov_map),
                             name="player")

        self.container = Container()

        self.container.add_system(self.action_system)
        self.container.add_system(self.ai_system)
        self.container.add_system(self.input_system)
        self.container.add_system(self.display_system)

        self.container.add_system(self.level_system)
        self.container.add_system(self.fov_system)

        self.container.add_entity(self.player)
        for entity in self.level_system.map.entities:
            self.container.add_entity(entity)

    def game_loop(self):
        self.container.update()
        self.player.get(FovComponent).fov_recalculate = True
        while not self.quit:
            self.container.update()


            if self.player.get(ActionComponent).action == "quit":
                self.quit = True

            pygame.display.flip()
            self.clock.tick(FPS)



if __name__ == '__main__':
    SiliconBlood().game_loop()
