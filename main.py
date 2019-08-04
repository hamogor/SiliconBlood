import pygame
from settings import TITLE, QUIT, S_ENEMY, WIDTH, HEIGHT, FPS

from ecs.container import Container
from ecs.display.display import DisplaySystem
from ecs.camera.camera import CameraSystem
from ecs.fov.fov import FovSystem
from ecs.keyboard.keyboard import KeyboardSystem
from ecs.movement.movement import MovementSystem
from ecs.level.level import LevelSystem
from ecs.action.action import ActionSystem
from actors.player import Player
import os


class SiliconBlood:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(S_ENEMY)
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.level = 1
        self.level_system = LevelSystem(self.level)  # First level
        self.player = Player(self.level_system.spawn_pos[0],
                             self.level_system.spawn_pos[1])
        self.keyboard_system = KeyboardSystem()
        self.action_system = ActionSystem(self.level_system)
        self.camera_system = CameraSystem(self.level_system)
        self.display_system = DisplaySystem(self.level_system, self.camera_system, self.display)
        self.fov_system = FovSystem(self.level_system)
        self.movement_system = MovementSystem(self.level_system)

        self.container = Container()
        self.container.add_system(self.keyboard_system)
        self.container.add_system(self.level_system)
        self.container.add_system(self.fov_system)
        self.container.add_system(self.display_system)
        self.container.add_system(self.movement_system)
        self.container.add_system(self.action_system)
        self.container.add_entity(self.player)

    def new_level(self):
        for system in self.container.systems:
            if getattr(system, "reset", None):
                system.reset(self.level_system)
                self.container.update()

    def game_loop(self):
        self.container.update()

        while not self.game_over:

            self.check_for_game_over()
            self.keyboard_system.update(self.container.entities)
            if self.keyboard_system.keys_pressed:
                self.movement_system.update(self.container.entities)
                self.fov_system.update(self.container.entities)
                self.display_system.update(self.container.entities)
                self.action_system.update(self.container.entities)
                if self.level_system.dungeon_level != self.level:
                    self.new_level()
                    self.level = self.level_system.dungeon_level
            self.clock.tick()

    def check_for_game_over(self):
        if self.keyboard_system.get_keys():
            keys_pressed = [e for e in self.keyboard_system.get_keys() if e == QUIT]
            if keys_pressed:
                self.game_over = True

    def check_if_time_passed(self):
        key_pressed = self.keyboard_system.get_keys()
        return key_pressed


if __name__ == '__main__':
    SiliconBlood().game_loop()
