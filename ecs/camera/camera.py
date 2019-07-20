from settings import CAM_WIDTH, CAM_HEIGHT, GRIDWIDTH, GRIDHEIGHT
from ecs.movement.movement_component import MovementComponent
from ecs.camera.camera_component import CameraComponent


class CameraSystem:
    def __init__(self, level):
        self.x = 0
        self.y = 0
        self.width = CAM_WIDTH
        self.height = CAM_HEIGHT
        self.map_width = level.level_map.width
        self.map_height = level.level_map.height

    def apply(self, x, y):
        x = x + self.x
        y = y + self.y
        return x, y

    def update(self, entities):
        for e in entities:
            if e.name == "player":
                x = e.get(MovementComponent).x - int(self.width / 2)
                y = e.get(MovementComponent).y - int(self.height / 2)
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                if x > GRIDWIDTH - CAM_WIDTH:
                    x = CAM_WIDTH
                if y > GRIDHEIGHT - CAM_HEIGHT:
                    y = CAM_HEIGHT
                self.x, self.y = x, y
                e.get(CameraComponent).cam_x = e.get(MovementComponent).x - self.x
                e.get(CameraComponent).cam_y = e.get(MovementComponent).y - self.y