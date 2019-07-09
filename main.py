from constants import *
from ecs.display.display import DisplaySystem
from ecs.human.player import Player
from ecs.input.keyboard import KeyboardInputSystem
from ecs.movement.movement import MovementSystem
from ecs.container import Container
import pygame


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(S_PLAYER)
        self.game_over = False

        self.player = Player()
        self.display_system = DisplaySystem()
        self.keyboard_input_system = KeyboardInputSystem()
        self.movement_system = MovementSystem(self.display_system.map.tiles)

        self.container = Container()
        self.container.add_system(self.keyboard_input_system)
        self.container.add_system(self.display_system)
        self.container.add_system(self.movement_system)
        self.container.add_entity(self.player)

    def game_loop(self):
        self.container.update()

        while not self.game_over:
            self.check_for_game_over()
            time_passed = self.check_if_time_passed()

            if time_passed:
                self.container.update()
            else:
                self.display_system.update(self.container._entities)
                self.keyboard_input_system.update(self.container._entities)
                self.movement_system.update(self.container._entities)

    def check_for_game_over(self):
        keys_pressed = [e for e in self.keyboard_input_system.get_all_keys_pressed() if e == QUIT]
        if keys_pressed:
            self.game_over = True

    def check_if_time_passed(self):
        all_keys_pressed = self.keyboard_input_system.get_all_keys_pressed()

        keys_pressed = [e for e in all_keys_pressed
                        if e == MOVE_N or e == MOVE_S or e == MOVE_W or e == MOVE_E]
        return keys_pressed


if __name__ == '__main__':
    Main().game_loop()
