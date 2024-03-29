from settings import CAM_WIDTH, CAM_HEIGHT, GRIDWIDTH, GRIDHEIGHT
from ecs.display.display_component import DisplayComponent
from ecs.camera.camera_component import CameraComponent


class CameraSystem:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = CAM_WIDTH
        self.height = CAM_HEIGHT
        self.map_width = GRIDWIDTH
        self.map_height = GRIDHEIGHT

    def reset(self):
        self.__init__()

    def apply(self, x, y):
        x = x + self.x
        y = y + self.y
        return int(x), int(y)

    def update(self, entity):
        if entity.has(CameraComponent):
            x = entity.get(DisplayComponent).x - int(self.width / 2)
            y = entity.get(DisplayComponent).y - int(self.height / 2)
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x > GRIDWIDTH - CAM_WIDTH:
                x = GRIDWIDTH - CAM_WIDTH
            if y > GRIDHEIGHT - CAM_HEIGHT:
                y = GRIDHEIGHT - CAM_HEIGHT
            self.x, self.y = x, y
            if entity.has(CameraComponent):
                entity.get(CameraComponent).cam_x = entity.get(DisplayComponent).x - self.x
                entity.get(CameraComponent).cam_y = entity.get(DisplayComponent).y - self.y
