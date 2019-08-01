from structs.tile import StrucTile
from structs.rect import Rect
from settings import *
import random
import pygame
import tcod as libtcod


class GameMap:
    '''
    A Binary Space Partition connected by a severely weighted
    drunkards walk algorithm.
    Requires Leaf and Rect classes.
    '''

    def __init__(self):
        self.level = []
        self.room = None
        self.MAX_LEAF_SIZE = 24
        self.ROOM_MAX_SIZE = 15
        self.ROOM_MIN_SIZE = 6
        self.smooth_edges = True
        self.smoothing = 1
        self.filling = 3
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self._leafs = []
        self.first_room = False
        self.tiles = self.generate_level()
        self.place_stairs()

    def generate_level(self):
        # Creates an empty 2D array or clears existing array
        
        self.level = [[StrucTile(True, True)
                       for _ in range(self.width)]
                      for _ in range(self.height)]

        root_leaf = Leaf(0, 0, self.width, self.height)
        self._leafs.append(root_leaf)

        split_successfully = True
        # loop through all leaves until they can no longer split successfully
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
        self.clean_up_map(self.width, self.height)
        for x in range(GRIDWIDTH):
            for y in range(GRIDHEIGHT):
                if self.level[x][y].sprite is None:
                    self.level[x][y].sprite = S_WALL
                    self.level[x][y].dark_sprite = S_DWALL
        return self.level

    def create_room(self, room):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y] = StrucTile(False, False, S_FLOOR, S_DFLOOR)
                if not self.first_room:
                    self.first_room = room.center()

    def place_stairs(self):
        last_room = self._leafs[-1]
        x, y = (last_room.room.center()[0], last_room.room.center()[1])
        self.tiles[x][y] = StrucTile(False, False, S_TELEPORTER, S_DSTAIRS, "stairs")

    def create_hall(self, room1, room2):
        # run a heavily weighted random Walk
        # from point2 to point1
        drunkard_x, drunkard_y = room2.center()
        goal_x, goal_y = room1.center()
        while not (room1.x1 <= drunkard_x <= room1.x2) or not (room1.y1 < drunkard_y < room1.y2):  #
            # ==== Choose Direction ====
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

            # ==== Walk ====
            # check collision at edges
            if (0 < drunkard_x + dx < self.width - 1) and (0 < drunkard_y + dy < self.height - 1):
                drunkard_x += dx
                drunkard_y += dy
                if self.level[int(drunkard_x)][int(drunkard_y)].block_path:
                    self.level[int(drunkard_x)][int(drunkard_y)] = StrucTile(False, False, S_FLOOR, S_DFLOOR)

    def clean_up_map(self, width, height):
        if self.smooth_edges:
            for i in range(3):
                # Look at each cell individually and check for smoothness
                for x in range(1, width - 1):
                    for y in range(1, height - 1):
                        if (self.level[x][y].block_path) and (self.get_adjacent_walls_simple(x, y) <= self.smoothing):
                            self.level[x][y] = StrucTile(False, False, S_FLOOR, S_DFLOOR)

                        if (not self.level[x][y].block_path) and (self.get_adjacent_walls_simple(x, y) >= self.filling):
                            self.level[x][y] = StrucTile(True, True, S_WALL, S_DWALL)

    def get_adjacent_walls_simple(self, x, y):  # finds the walls in four directions
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


class Leaf:  # used for the BSP tree algorithm
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.MIN_LEAF_SIZE = 10
        self.room_1 = None
        self.room_2 = None
        self.child_1 = None
        self.child_2 = None
        self.room = None
        self.hall = None

    def split_leaf(self):
        # begin splitting the leaf into two children
        if (self.child_1 is not None) or (self.child_2 is not None):
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
            max_ = self.height - self.MIN_LEAF_SIZE
        else:
            max_ = self.width - self.MIN_LEAF_SIZE
        if max_ <= self.MIN_LEAF_SIZE:
            return False  # the leaf is too small to split further
        split = random.randint(self.MIN_LEAF_SIZE, max_)  # determine where to split the leaf
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
                bsp_tree.create_hall(self.child_1.maxget_room(),
                                     self.child_2.maxget_room())
        else:
            # Create rooms in the end branches of the bsp tree
            w = random.randint(bsp_tree.ROOM_MIN_SIZE, min(bsp_tree.ROOM_MAX_SIZE, self.width - 1))
            h = random.randint(bsp_tree.ROOM_MIN_SIZE, min(bsp_tree.ROOM_MAX_SIZE, self.height - 1))
            x = random.randint(self.x, self.x + (self.width - 1) - w)
            y = random.randint(self.y, self.y + (self.height - 1) - h)
            self.room = Rect(x, y, w, h)
            bsp_tree.create_room(self.room)

    def maxget_room(self):
        if self.room:
            return self.room
        else:
            if self.child_1:
                self.room_1 = self.child_1.maxget_room()
            if self.child_2:
                self.room_2 = self.child_2.maxget_room()
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
