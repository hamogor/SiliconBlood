from constants import *
from display.display import DisplaySystem
from display.display_component import DisplayComponent
from input.keyboard import KeyboardInputSystem
from input.keyboard_input_component import KeyboardInputComponent
from ecs.entity import Entity
from ecs.container import Container
import pygame
import pysnooper


class Player(Entity):
    def __init__(self):
        super().__init__(DisplayComponent(S_PLAYER, 0, 0))
        self.set(KeyboardInputComponent(self._process_input))

    def _process_input(self, keys_pressed):
        for key_pressed in keys_pressed:
            if key_pressed in MOVE_N:
                self.get(DisplayComponent).y -= 1 * TILESIZE
            elif key_pressed in MOVE_S:
                self.get(DisplayComponent).y += 1 * TILESIZE
            elif key_pressed in MOVE_W:
                self.get(DisplayComponent).x -= 1 * TILESIZE
            elif key_pressed in MOVE_E:
                self.get(DisplayComponent).x += 1 * TILESIZE
            else:
                print("You pressed {}".format(key_pressed))



class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.player = Player()
        self.game_over = False

        self.display_system = DisplaySystem()
        self.keyboard_input_system = KeyboardInputSystem()

        self.container = Container()

        self.container.add_system(self.keyboard_input_system)
        self.container.add_system(self.display_system)
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
