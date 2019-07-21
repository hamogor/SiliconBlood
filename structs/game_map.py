from structs.tile import StrucTile
from structs.rect import Rect
from settings import *
import random
import tcod
import pysnooper


class GameMap:
    def __init__(self):
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self.tiles = self.generate_ca_level()
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
        return new_map

    def generate_ca_level(self):
        tiles = [[StrucTile(False, False) for y in range(self.height)] for x in range(self.width)]
        cell_map = self.cellular_gen(tiles)
        for i in range(8):
            cell_map = self.do_gen_step(cell_map)
        return cell_map

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

