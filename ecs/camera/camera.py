from constants import *
from ecs.movement.movement_component import MovementComponent
from ecs.camera.camera_component import CameraComponent


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = CAM_WIDTH
        self.height = CAM_HEIGHT
        self.map_width = GRIDWIDTH
        self.map_height = GRIDHEIGHT

    def apply(self, x, y):
        x = x + self.x
        y = y + self.y
        return x, y

    def update(self, player):
        x = player.get(MovementComponent).x - int(self.width / 2)
        y = player.get(MovementComponent).y - int(self.height / 2)
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > GRIDWIDTH - CAM_WIDTH:
            x = CAM_WIDTH
        if y > GRIDHEIGHT - CAM_HEIGHT:
            y = CAM_HEIGHT
        self.x, self.y = x, y
        player.get(CameraComponent).cam_x = player.get(MovementComponent).x - self.x
        player.get(CameraComponent).cam_y = player.get(MovementComponent).y - self.y