import tcod as libtcod
from settings import GRIDWIDTH, GRIDHEIGHT, S_WALL, S_FLOOR, S_FOG, S_STAIRS
import random
from utils.map_utils import check_for_wall
from structs.tile import Tile
from structs.assets import Assets


class GameMap:
    def __init__(self):
        self.map_width = GRIDWIDTH
        self.map_height = GRIDHEIGHT
        self.MAX_LEAF_SIZE = 14
        self.ROOM_MAX_SIZE = 10
        self.ROOM_MIN_SIZE = 6
        self.smoothEdges = True
        self.smoothing = 1
        self.filling = 3
        self._leafs = []
        self.level = self.generate_level()
        self.spawn = self.place_entrance_exit()
        print(self.spawn)

    def initialize_tiles(self):
        return [[Tile(True, True)
                 for _ in range(self.map_width)]
                for _ in range(self.map_width)]

    def generate_level(self):
        self.level = self.initialize_tiles()

        root_leaf = Leaf(0, 0, self.map_width, self.map_height)
        self._leafs.append(root_leaf)

        split_successfully = True
        while split_successfully:
            split_successfully = False
            for leaf in self._leafs:
                if not leaf.child_1 and not leaf.child_2:
                    if ((leaf.width > self.MAX_LEAF_SIZE) or
                            (leaf.height > self.MAX_LEAF_SIZE) or
                            (random.random() > 0.8)):
                        if leaf.split_leaf():
                            self._leafs.append(leaf.child_1)
                            self._leafs.append(leaf.child_2)
                            split_successfully = True

        root_leaf.create_rooms(self)
        self.clean_up_map()
        self.assign_tiles()

        return self.level

    def place_entrance_exit(self):
        stairs_x, stairs_y = self._leafs[-1].room.center()
        spawn_x, spawn_y = self._leafs[0].room.center()
        self.level[stairs_x][stairs_y] = Tile(False, False, S_STAIRS, "stairs")
        return spawn_x, spawn_y

    def create_room(self, room):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y] = Tile(False, False, S_FLOOR)

    def create_hall(self, room1, room2):
        drunkard_x, drunkard_y = room2.center()
        goal_x, goal_y = room1.center()
        while not (room1.x1 <= drunkard_x <= room1.x2) or not (room1.y1 < drunkard_y < room1.y2):
            north = 1.0
            south = 1.0
            east = 1.0
            west = 1.0

            weight = 1

            # weight the random walk against edges
            if drunkard_x < goal_x:  # drunkard is left of point1
                east += weight
            elif drunkard_x > goal_x:  # drunkard is right of point1
                west += weight
            if drunkard_y < goal_y:  # drunkard is above point1
                south += weight
            elif drunkard_y > goal_y:  # drunkard is below point1
                north += weight

                # normalize probabilities so they form a range from 0 to 1
                total = north + south + east + west
                north /= total
                south /= total
                east /= total
                west /= total

                # choose the direction
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

                # check colision at edges
                if (0 < drunkard_x + dx < self.map_width - 1) and (0 < drunkard_y + dy < self.map_height - 1):
                    drunkard_x += dx
                    drunkard_y += dy
                    if self.level[int(drunkard_x)][int(drunkard_y)].block_path:
                        self.level[int(drunkard_y)][int(drunkard_y)] = Tile(False, False, S_FLOOR)

    def clean_up_map(self):
        if self.smoothEdges:
            for i in range(3):
                for x in range(1, self.map_width - 1):
                    for y in range(1, self.map_height - 2):
                        if self.level[x][y].block_path and (self.get_adjacent_walls_simple(x, y) <= self.smoothing):
                            self.level[x][y] = Tile(False, False, S_FLOOR)

                        if (not self.level[x][y].block_path) and (self.get_adjacent_walls_simple(x, y) >= self.filling):
                            self.level[x][y] = Tile(True, True, S_WALL)

    def get_adjacent_walls_simple(self, x, y):
        wall_counter = 0
        # print("(",x,",",y,") = ",self.level[x][y])
        if self.level[x][y - 1].block_path:  # Check north
            wall_counter += 1
        if self.level[x][y + 1].block_path:  # Check south
            wall_counter += 1
        if self.level[x - 1][y].block_path:  # Check west
            wall_counter += 1
        if self.level[x + 1][y].block_path:  # Check east
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

    def fill_fog(self):
        for x in range(GRIDWIDTH):
            for y in range(GRIDHEIGHT):
                if not self.level[x][y].sprite:
                    self.level[x][y] = Tile(True, True, S_FOG)


class Rect:  # used for the tunneling algorithm
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return int(center_x), int(center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Leaf:  # used for the BSP tree algorithm
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.MIN_LEAF_SIZE = 10
        self.child_1 = None
        self.child_2 = None
        self.room = None
        self.room_1, self.room_2 = None, None
        self.hall = None

    def split_leaf(self):
        # begin splitting the leaf into two children
        if not self.child_1 or not self.child_2:
            return False  # This leaf has already been split

        '''
        ==== Determine the direction of the split ====
        If the width of the leaf is >25% larger than the height,
        split the leaf vertically.
        If the height of the leaf is >25 larger than the width,
        split the leaf horizontally.
        Otherwise, choose the direction at random.
        '''
        split_horizontally = random.choice([True, False])
        if self.width / self.height >= 1.25:
            split_horizontally = False
        elif self.height / self.width >= 1.25:
            split_horizontally = True

        if split_horizontally:
            _max = self.height - self.MIN_LEAF_SIZE
        else:
            _max = self.width - self.MIN_LEAF_SIZE

        if _max <= self.MIN_LEAF_SIZE:
            return False  # the leaf is too small to split further

        split = random.randint(self.MIN_LEAF_SIZE, _max)  # determine where to split the leaf

        if split_horizontally:
            self.child_1 = Leaf(self.x, self.y, self.width, split)
            self.child_2 = Leaf(self.x, self.y + split, self.width, self.height - split)
        else:
            self.child_1 = Leaf(self.x, self.y, split, self.height)
            self.child_2 = Leaf(self.x + split, self.y, self.width - split, self.height)

        return True

    def create_rooms(self, bsp_tree):
        if self.child_1 or self.child_2:
            # recursively search for children until you hit the end of the branch
            if self.child_1:
                self.child_1.create_rooms(bsp_tree)
            if self.child_2:
                self.child_2.create_rooms(bsp_tree)

            if self.child_1 and self.child_2:
                bsp_tree.create_hall(self.child_1.get_room(),
                                     self.child_2.get_room())

        else:
            # Create rooms in the end branches of the bsp tree
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
            if self.child_1:
                self.room_1 = self.child_1.get_room()
            if self.child_2:
                self.room_2 = self.child_2.get_room()

            if not self.child_1 and not self.child_2:
                # neither room_1 nor room_2
                return None

            elif not self.room_2:
                # room_1 and !room_2
                return self.room_1

            elif not self.room_1:
                # room_2 and !room_1
                return self.room_2

            # If both room_1 and room_2 exist, pick one
            elif random.random() < 0.5:
                return self.room_1
            else:
                return self.room_2
