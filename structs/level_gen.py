import random
from structs.assets import Assets
from utils.map_utils import check_for_wall
from structs.tile import Tile
from settings import GRIDWIDTH, GRIDHEIGHT, S_STAIRS, S_FLOOR, S_ENEMY
from structs.actor import Actor
from ecs.display.display_component import DisplayComponent


class LevelGenerator:
    def __init__(self):
        self.map_width = GRIDWIDTH
        self.map_height = GRIDHEIGHT
        self.MAX_LEAF_SIZE = 24
        self.ROOM_MAX_SIZE = 11
        self.ROOM_MIN_SIZE = 6
        self.smooth_edges = True
        self.smoothing = 1
        self.filling = 3
        self._leafs = []
        self.tiles = self.generate_level()
        self.assign_tiles()
        self.spawn = self.place_entrance_exit()
        self.entities = self.place_entities()

    def generate_level(self):
        self.level = [[Tile(True, True)
                       for _ in range(self.map_width)]
                      for _ in range(self.map_height)]

        root_leaf = Leaf(0, 0, self.map_width, self.map_height)
        self._leafs.append(root_leaf)

        split_successfully = True
        while split_successfully:
            split_successfully = False
            for l in self._leafs:
                if l.child_1 is None and l.child_2 is None:
                    if ((l.width > self.MAX_LEAF_SIZE) or
                            (l.height > self.MAX_LEAF_SIZE) or
                            (random.random() > 0.8)):
                        if l.split_leaf():  # try to split the leaf
                            self._leafs.append(l.child_1)
                            self._leafs.append(l.child_2)
                            split_successfully = True

        root_leaf.create_rooms(self)
        self.clean_up_map()
        self.assign_tiles()
        return self.level

    def place_entities(self):
        entities = []
        for i in range(len(self._leafs)):
            room_center = self._leafs[i].get_room().center()
            npc = Actor(DisplayComponent(S_ENEMY, room_center[0], room_center[1], alpha=True),
                        name="npc")

            entities.append(npc)
        return entities

    def place_entrance_exit(self):
        stairs_x, stairs_y = self._leafs[-1].get_room().center()
        spawn_x, spawn_y = self._leafs[0].get_room().center()
        #self.level[int(spawn_x)][int(spawn_y)] = Tile(False, False, S_STAIRS, "stairs")
        self.level[int(stairs_x)][int(stairs_y)] = Tile(False, False, S_STAIRS, "stairs")
        return int(spawn_x), int(spawn_y)

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y] = Tile(False, False)

    def create_hall(self, room1, room2):
        drunkard_x, drunkard_y = room2.center()
        goal_x, goal_y = room1.center()
        while not (room1.x1 <= drunkard_x <= room1.x2) or not (room1.y1 < drunkard_y < room1.y2):
            north = 1.0
            south = 1.0
            east = 1.0
            west = 1.0

            weight = 1

            if drunkard_x < goal_x:
                east += weight
            elif drunkard_x > goal_x:
                west += weight
            elif drunkard_y < goal_y:
                south += weight
            elif drunkard_y > goal_y:
                north += weight

            total = north + south + east + west
            north /= total
            south /= total
            east /= total
            west /= total

            choice = random.random()
            if 0 <= choice < north:
                dx = 0
                dy = -1
            elif north <= choice < (north + south):
                dx = 0
                dy = 1
            elif (north + south) <= choice < (north + south + east):
                dx = 1
                dy = 0
            else:
                dx = -1
                dy = 0

            if (0 < drunkard_x + dx < self.map_width - 1) and \
               (0 < drunkard_y + dy < self.map_height - 1):
                drunkard_x += dx
                drunkard_y += dy
                if self.level[int(drunkard_x)][int(drunkard_y)].block_path:
                    self.level[int(drunkard_x)][int(drunkard_y)] = Tile(False, False)

    def clean_up_map(self):
        if self.smooth_edges:
            for i in range(3):
                # Look at each cell individually and check for smoothness
                for x in range(1, self.map_width - 1):
                    for y in range(1, self.map_height - 1):
                        if self.level[x][y].block_path and (self.get_adjacent_walls_simple(x, y) <= self.smoothing):
                            self.level[x][y] = Tile(False, False)

                        if (not self.level[x][y].block_path) and (self.get_adjacent_walls_simple(x, y) >= self.filling):
                            self.level[x][y] = Tile(True, True)

    def get_adjacent_walls_simple(self, x, y):
        wall_counter = 0
        if self.level[x][y - 1].block_path:
            wall_counter += 1
        if self.level[x][y + 1].block_path:
            wall_counter += 1
        if self.level[x - 1][y].block_path:
            wall_counter += 1
        if self.level[x + 1][y].block_path:
            wall_counter += 1

        return wall_counter

    def assign_tiles(self):
        # loop through map looking for the walls, then assign bit-operator
        assets = Assets()
        for x in range(len(self.level)):
            for y in range(len(self.level[0])):

                # check tile for wall status
                tile_is_wall = check_for_wall(x, y, self.level)

                if tile_is_wall:
                    # create tile var
                    tile_assignment = 0
                    # add bit-mask value
                    if check_for_wall(x, y - 1, self.level):
                        tile_assignment += 1
                    if check_for_wall(x + 1, y, self.level):
                        tile_assignment += 2
                    if check_for_wall(x, y + 1, self.level):
                        tile_assignment += 4
                    if check_for_wall(x - 1, y, self.level):
                        tile_assignment += 8
                    self.level[x][y].sprite = assets.wall_dict[tile_assignment]
                    self.level[x][y].assignment = tile_assignment
                    if self.level[x][y].assignment == 15:
                        self.level[x][y].unexplorable = True
                else:
                    self.level[x][y].sprite = S_FLOOR


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return int(center_x), int(center_y)

    def interset(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Leaf:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.MIN_LEAF_SIZE = 10
        self.child_1 = None
        self.child_2 = None
        self.hall = None
        self.room = None  # Not in original may cause bugs
        self.room_1, self.room_2 = None, None  # Not in original may cause bugs

    def split_leaf(self):
        if self.child_1 or self.child_2:
            return False

        split_horizontally = random.choice([True, False])
        if self.width / self.height >= 1.25:
            split_horizontally = False
        elif self.height / self.width >= 1.25:
            split_horizontally = True

        if split_horizontally:
            max_ = self.height - self.MIN_LEAF_SIZE
        else:
            max_ = self.width - self.MIN_LEAF_SIZE

        if max_ <= self.MIN_LEAF_SIZE:
            return False

        split = random.randint(self.MIN_LEAF_SIZE, max_)

        if split_horizontally:
            self.child_1 = Leaf(self.x, self.y, self.width, split)
            self.child_2 = Leaf(self.x, self.y + split, self.width, self.height - split)
        else:
            self.child_1 = Leaf(self.x, self.y, split, self.height)
            self.child_2 = Leaf(self.x + split, self.y, self.width - split, self.height)

        return True

    def create_rooms(self, bsp_tree):
        if self.child_1 or self.child_2:
            if self.child_1:
                self.child_1.create_rooms(bsp_tree)
            if self.child_2:
                self.child_2.create_rooms(bsp_tree)

            if self.child_1 and self.child_2:
                bsp_tree.create_hall(self.child_1.get_room(),
                                     self.child_2.get_room())

        else:
            w = random.randint(bsp_tree.ROOM_MIN_SIZE, min(bsp_tree.ROOM_MAX_SIZE, self.width - 1))
            h = random.randint(bsp_tree.ROOM_MIN_SIZE, min(bsp_tree.ROOM_MAX_SIZE, self.height - 1))
            x = random.randint(self.x, self.x + (self.width - 1) - w)
            y = random.randint(self.y, self.y + (self.height - 1) - h)
            self.room = Rect(x, y, w, h)
            bsp_tree.create_room(self.room)

    def get_room(self):
        if self.room:
            return self.room
        else:
            if self.child_2:
                self.room_1 = self.child_1.get_room()
            if self.child_2:
                self.room_2 = self.child_2.get_room()

            if not self.child_1 and not self.child_2:
                return None
            elif not self.room_2:
                return self.room_1
            elif not self.room_1:
                return self.room_2

            elif random.random() < 0.5:
                return self.room_1
            else:
                return self.room_2
