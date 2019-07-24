from structs.tile import StrucTile
from structs.rect import Rect
from settings import *
import random
from pprint import pprint as pp
import tcod
import pysnooper


class GameMap:
    __slots__ = ['width', 'height', 'tiles', 'list_rooms', 'list_regions', 'list_objects']

    def __init__(self):
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        #self.tiles = self.generate_ca_level()
        self.tiles = BspTree().generate_level()
        for tile in self.tiles[0]:
            print(tile.__dict__)
        self.list_rooms = []
        self.list_regions = []
        self.list_objects = []

        self.make_map()

    def init_tiles(self):
        tiles = [[StrucTile(True, True) for y in range(self.height)] for x in range(self.width)]
        for x in range(0, self.width):
            for y in range(0, self.height):
                tiles[x][y].sprite, tiles[x][y].dark_sprite = S_WALL, S_DWALL
        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_path:
            return True

        return False

    def cellular_gen(self, tiles):
        chance_to_live = float(0.68)
        for x in range(self.width):
            for y in range(self.height):
                if random.uniform(0, 1) > chance_to_live:
                    tiles[x][y].block_path, tiles[x][y].block_sight = True, True
        return tiles

    def count_alive_neighbours(self, tiles, x, y):
        count = 0
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                neighbour_x = x + i
                neighbour_y = y + j
                if i == 0 and j == 0:
                    pass
                elif neighbour_x < 0 or neighbour_y < 0 \
                        or neighbour_x >= self.width or neighbour_y >= self.height:
                    count += 1
                elif tiles[neighbour_x][neighbour_y].block_path:
                    count += 1
        return count

    def do_gen_step(self, old_map):
        new_map = [[StrucTile(False, False) for y in range(self.height)] for x in range(self.width)]
        stairs = False
        for x in range(self.width):
            for y in range(self.height):
                neighbours = self.count_alive_neighbours(old_map, x, y)
                if old_map[x][y].block_path:
                    new_map[x][y].block_path = neighbours >= 3
                    new_map[x][y].sprite = S_WALL
                    new_map[x][y].dark_sprite = S_DWALL

                else:
                    new_map[x][y].block_path = neighbours > 4
                    new_map[x][y].sprite = S_FLOOR
                    new_map[x][y].dark_sprite = S_DFLOOR
                    if random.randint(0, 1) == 1 and not stairs:
                        new_map[x][y].sprite = S_STAIRS
                        stairs = True
        return new_map

    def generate_ca_level(self):
        tiles = [[StrucTile(False, False) for y in range(self.height)] for x in range(self.width)]
        cell_map = self.cellular_gen(tiles)
        for i in range(8):
            cell_map = self.do_gen_step(cell_map)
        return cell_map

    # Normal generation #
    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].block_path = False
                self.tiles[x][y].block_sight = False
                self.tiles[x][y].sprite = S_FLOOR
                self.tiles[x][y].dark_sprite = S_DFLOOR

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False
            self.tiles[x][y].sprite = S_FLOOR
            self.tiles[x][y].dark_sprite = S_DFLOOR

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].block_path = False
            self.tiles[x][y].block_sight = False
            self.tiles[x][y].sprite = S_FLOOR
            self.tiles[x][y].dark_sprite = S_DFLOOR

    def make_map(self):
        rooms = []
        room_max_size = 10
        room_min_size = 6
        max_rooms = 30
        num_rooms = 0

        for r in range(max_rooms):
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)

            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
                else:
                    self.create_room(new_room)

                    new_x, new_y = new_room.center()

                    # TODO - Create player spawn room
                    if num_rooms == 0:
                        #player.x = new_x
                        #plyer.y = new_y
                        pass
                    else:
                        prev_x, prev_y = rooms[num_rooms - 1].center()

                        if random.randint(0, 1) == 1:
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_x, new_x, new_y)

                    rooms.append(new_room)
                    num_rooms += 1


class BspTree:
    def __init__(self):
        self.room = None
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self._leafs = []
        self.MAX_LEAF_SIZE = 35
        self.ROOM_MAX_SIZE = 20
        self.ROOM_MIN_SIZE = 8
        self.level = []

    def generate_level(self):
        # Creates an empty 2D array or clears existing array
        self.level = [[StrucTile(True, True) for y in range(self.height)] for x in range(self.width)]
        root_leaf = Leaf(0, 0, self.width, self.height)
        
        self._leafs.append(root_leaf)
        split_successfully = True
        # loop through all leaves until they can no longer split successfully
        while split_successfully:
            split_successfully = False
            for l in self._leafs:
                if (l.child_1 is None) and (l.child_2 is None):
                    if ((l.width > self.MAX_LEAF_SIZE) or
                            (l.height > self.MAX_LEAF_SIZE) or
                            (random.random() > 0.8)):
                        if l.split_leaf():  # try to split the leaf
                            self._leafs.append(l.child_1)
                            self._leafs.append(l.child_2)
                            split_successfully = True
        root_leaf.create_rooms(self)
        self.fill_map()
        return self.level

    def create_room(self, room):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y].block_path = False
                self.level[x][y].block_sight = False
                self.level[x][y].sprite = S_FLOOR
                self.level[x][y].dark_sprite = S_DFLOOR

    def create_hall(self, room1, room2):
        # connect two rooms by hallways
        x1, y1 = room1.center()
        x2, y2 = room2.center()
        # 50% chance that a tunnel will start horizontally
        if random.randint(0, 1) == 1:
            self.create_h_tunnel(x1, x2, y1)
            self.create_v_tunnel(y1, y2, x2)
        else:  # else it starts vertically
            self.create_v_tunnel(y1, y2, x1)
            self.create_h_tunnel(x1, x2, y2)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.level[x][y].block_path = False
            self.level[x][y].block_sight = False
            self.level[x][y].sprite = S_FLOOR
            self.level[x][y].dark_sprite = S_DFLOOR

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.level[x][y].block_path = False
            self.level[x][y].block_sight = False
            self.level[x][y].sprite = S_FLOOR
            self.level[x][y].dark_sprite = S_DFLOOR

    def fill_map(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.level[x][y].sprite is None:
                    self.level[x][y].sprite = S_WALL
                    self.level[x][y].dark_sprite = S_DWALL


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
