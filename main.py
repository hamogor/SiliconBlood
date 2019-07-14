from constants import *
from ecs.display.display import DisplaySystem
from ecs.human.player import Player
from ecs.input.keyboard import KeyboardInputSystem
from ecs.movement.movement import MovementSystem
from ecs.fov.fov import FovSystem
from ecs.container import Container
import pygame
import pysnooper


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(S_PLAYER)
        self.game_over = False

        self.player = Player()
        self.display_system = DisplaySystem()
        self.fov_system = FovSystem(self.display_system.map.tiles)
        self.keyboard_input_system = KeyboardInputSystem()
        self.movement_system = MovementSystem(self.display_system.map.tiles)

        self.container = Container()
        self.container.add_system(self.keyboard_input_system)
        self.container.add_system(self.movement_system)
        self.container.add_system(self.fov_system)
        self.container.add_system(self.display_system)
        self.container.add_entity(self.player)

    def game_loop(self):
        self.container.update()

        while not self.game_over:
            self.check_for_game_over()
            time_passed = self.check_if_time_passed()

            if time_passed:
                self.container.update()
                print("update")

    def check_for_game_over(self):
        if self.keyboard_input_system.get_all_keys_pressed():
            keys_pressed = [e for e in self.keyboard_input_system.get_all_keys_pressed() if e == QUIT]
            if keys_pressed:
                self.game_over = True

    def check_if_time_passed(self):
        key_pressed = self.keyboard_input_system.get_all_keys_pressed()

        return key_pressed


if __name__ == '__main__':
    Main().game_loop()
