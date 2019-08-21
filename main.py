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
import time


class SiliconBlood:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(S_PLAYER)
        pygame.key.set_repeat(200, 40)
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.quit = False
        self.dungeon_level = 1

        self.level_system = LevelSystem(self.dungeon_level)

        self.input_system = InputSystem()
        self.display_system = DisplaySystem(self.level_system, self.display)
        self.fov_system = FovSystem(self.level_system)

        self.action_system = ActionSystem(self.level_system)

        self.player = Actor(DisplayComponent(self.level_system.map.spawn[0],
                                             self.level_system.map.spawn[1],
                                             S_PLAYER, alpha=True),
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

    def new_level(self):
        for system in self.container.systems:
            if getattr(system, "reset", None):
                system.reset(self.level_system)
        self.player.get(DisplayComponent).x, self.player.get(DisplayComponent).y = self.level_system.map.spawn
        print(self.level_system.map.spawn)
        for x in range(GRIDWIDTH):
            for y in range(GRIDHEIGHT):
                self.level_system.map.level[x][y].explored = False
        pygame.display.flip()
        #self.display_system.transition_out()
        self.display_system.transition()
        self.container.update()
        #self.display_system.transition_in()

    def game_loop(self):
        self.container.update()
        while not self.quit:
            self.input_system.update(self.container.entities)
            self.action_system.update(self.container.entities)
            self.fov_system.update(self.container.entities)
            self.display_system.update(self.container.entities)
            self.level_system.update(self.container.entities)
            if self.level_system.dungeon_level != self.dungeon_level:
                self.new_level()
                self.dungeon_level = self.level_system.dungeon_level

            if self.player.get(ActionComponent).action == ("quit", ""):
                self.quit = True


if __name__ == '__main__':
    SiliconBlood().game_loop()
