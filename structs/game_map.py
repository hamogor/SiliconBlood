from settings import MAPHEIGHT, MAPWIDTH
from structs.tile import Tile
import tcod as libtcod
import random

class GameMap:
    def __init__(self):
        self.level = []

        self.ROOM_MAX_SIZE = 18
        self.ROOM_MIN_SIZE = 16
        self.MAX_NUM_ROOMS = 30

        self.SQUARE_ROOM_MAX_SIZE = 12
        self.SQUARE_ROOM_MIN_SIZE = 6

        self.CROSS_ROOM_MAX_SIZE = 12
        self.CROSS_ROOM_MIN_SIZE = 6

        self.cavern_chance = 0.40
        self.CAVERN_MAX_SIZE = 35

        self.wall_probability = 0.45
        self.neighbours = 4

        self.square_room_chance = 0.2
        self.cross_room_chance = 0.15

        self.build_room_attempts = 500
        self.place_room_attempts = 20
        self.max_tunnel_length = 12

        self.include_shortcuts = True
        self.shortcut_attempts = 500
        self.shortcut_length = 5
        self.min_pathfinding_distance = 50
        self.rooms = []
        self.tiles = self.generate_level()

    def generate_level(self):
        self.level = [[Tile(True, True)
                       for x in range(MAPWIDTH)]
                      for y in range(MAPHEIGHT)]

        room = self.generate_room()
        room_width, room_height = self.get_room_dimensions(room)
        room_x = (MAPWIDTH / 2 - room_width / 2) - 1
        room_y = (MAPHEIGHT / 2 - room_height / 2) - 1
        self.add_room(room_x, room_y, room)

        for i in range(self.build_room_attempts):
            room = self.generate_room()
            room_x, room_y, wall_tile, direction, tunnel_length = self.place_room(room)
            if room_x and room_y:
                self.add_room(room_x, room_y, room)
                self.add_tunnel(wall_tile, direction, tunnel_length)
                if len(self.rooms) >= self.MAX_NUM_ROOMS:
                    break

        if self.include_shortcuts:
            self.add_shortcuts(MAPWIDTH, MAPHEIGHT)

        return self.tiles

    def generate_room(self):
        if self.rooms:
            choice = random.random()

            if choice < self.square_room_chance:
                room = self.generate_room_square()
            elif self.square_room_chance <= choice < (self.square_room_chance * self.cross_room_chance):
                room = self.generate_room_cross()
            else:
                room = self.generate_room_ca()

        else:
            choice = random.random()
            if choice < self.cavern_chance:
                room = self.generate_room_cavern()
            else:
                room = self.generate_room_square()

        return room

    def generate_room_cross(self):
        room_h_width = (random.randint(self.CROSS_ROOM_MIN_SIZE + 2, self.CROSS_ROOM_MAX_SIZE)) / 2 * 2
        room_vir_height = (random.randint(self.CROSS_ROOM_MIN_SIZE + 2, self.CROSS_ROOM_MAX_SIZE)) / 2 * 2
        room_hor_height = (random.randint(self.CROSS_ROOM_MIN_SIZE, room_vir_height - 2)) / 2 * 2
        room_vir_width = (random.randint(self.CROSS_ROOM_MIN_SIZE, room_h_width - 2)) / 2 * 2

        room = [[Tile(True, True)
                 for x in range(room_vir_height)]
                for y in range(room_h_width)]

        vir_offset = room_vir_height / 2 - room_hor_height / 2
        for y in range(int(vir_offset), int(room_hor_height) + int(vir_offset)):
            for x in range(0, int(room_h_width)):
                room[x][y].block_path = False

        return room

    def generate_room_square(self):
        room_width = random.randint(self.SQUARE_ROOM_MIN_SIZE, self.SQUARE_ROOM_MAX_SIZE)
        room_height = random.randint(max(int(room_width * 0.5), self.SQUARE_ROOM_MIN_SIZE),
                                     min(int(room_width * 1.5), self.SQUARE_ROOM_MAX_SIZE))

        room = [[Tile(True, True)
                 for x in range(room_height)]
                for y in range(room_width)]

        room = [[Tile(False, False)
                 for x in range(1, room_height - 1)]
                for y in range(1, room_width - 1)]

        return room

    def generate_room_ca(self):
        while True:
            room = [[Tile(True, True)
                 for x in range(self.ROOM_MAX_SIZE)]
                for y in range(self.ROOM_MIN_SIZE)]

            for y in range(2, self.ROOM_MAX_SIZE - 2):
                for x in range(2, self.ROOM_MAX_SIZE - 2):
                    if random.random() >= self.wall_probability:
                        room[x][y] = Tile(False, False)

            for i in range(4):
                for y in range(1, self.ROOM_MAX_SIZE - 1):
                    for x in range(1, self.ROOM_MAX_SIZE - 1):
                        if self.get_adjacent_walls(x, y, room) > self.neighbours:
                            room[x][y] = Tile(True, True)
                        elif self.get_adjacent_walls(x, y, room) < self.neighbours:
                            room[x][y] = Tile(False, False)

            room = self.flood_fill(room)

            room_width, room_height = self.get_room_dimensions(room)
            for x in range(room_width):
                for y in range(room_height):
                    if not room[x][y].block_path:
                        return room

    def generate_room_cavern(self):
        while True:
            room = [[Tile(True, True)
                 for x in range(self.ROOM_MAX_SIZE)]
                for y in range(self.ROOM_MIN_SIZE)]

            for y in range(2, self.CAVERN_MAX_SIZE - 2):
                for x in range(2, self.CAVERN_MAX_SIZE - 2):
                    print(x, y)
                    if random.random() >= self.wall_probability:
                        room[x][y] = Tile(False, False)

            for i in range(4):
                for y in range(1, self.CAVERN_MAX_SIZE - 1):
                    for x in range(1, self.CAVERN_MAX_SIZE - 1):
                        if self.get_adjacent_walls(x, y, room) > self.neighbours:
                            room[x][y] = Tile(True, True)
                        elif self.get_adjacent_walls(x, y, room) < self.neighbours:
                            room[x][y] = Tile(False, False)

            room = self.flood_fill(room)

            room_width, room_height = self.get_room_dimensions(room)
            for x in range(room_width):
                for y in range(room_height):
                    if not room[x][y].block_path:
                        return room

    def flood_fill(self, room):
        room_width, room_height = self.get_room_dimensions(room)
        largest_region = set()

        for x in range(room_width):
            for y in range(room_height):
                if not room[x][y].block_path:
                    new_region = set()
                    tile = (x, y)
                    to_be_filled = set([tile])
                    while to_be_filled:
                        tile = to_be_filled.pop()

                        if tile not in new_region:
                            new_region.add(tile)

                            room[tile[0]][tile[1]] = Tile(True, True)
                            x = tile[0]
                            y = tile[1]
                            north = (x, y - 1)
                            south = (x, y + 1)
                            east = (x + 1, y)
                            west = (x - 1, y)

                            for direction in [north, south, east, west]:

                                if not room[direction[0]][direction[1]].block_path:
                                    if direction not in to_be_filled and direction not in new_region:
                                        to_be_filled.add(direction)

                    if len(new_region) >= self.ROOM_MIN_SIZE:
                        if len(new_region) > len(largest_region):
                            largest_region.clear()
                            largest_region.update(new_region)

        for tile in largest_region:
            room[tile[0]][tile[1]] = Tile(False, False)

        return room

    def place_room(self, room):
        room_width, room_height = self.get_room_dimensions(room)

        for i in range(self.place_room_attempts):
            wall_tile = None
            direction = self.get_direction()
            while not wall_tile:
                tile_x = random.randint(1, MAPWIDTH - 2)
                tile_y = random.randint(1, MAPHEIGHT - 1)
                if (self.level[tile_x][tile_y].block_path and
                    self.level[tile_x + direction[0]][tile_y + direction[1]].block_path and
                    not self.level[tile_x - direction[0]][tile_y - direction[1]].block_path):
                        wall_tile = (tile_x, tile_y)

            start_room_x = None
            start_room_y = None

            while not start_room_x and not start_room_y:
                x = random.randint(0, room_width - 1)
                y = random.randint(0, room_height - 1)
                if not room[x][y].block_path:
                    start_room_x = wall_tile[0] - x
                    start_room_y = wall_tile[1] - y

            for tunnel_length in range(self.max_tunnel_length):
                possible_room_x = start_room_x + direction[0] * tunnel_length
                possible_room_y = start_room_y + direction[1] * tunnel_length

                enough_room = self.get_overlap(room, possible_room_x, possible_room_y)

                if enough_room:
                    room_x = possible_room_x
                    room_y = possible_room_y

                    return room_x, room_y, wall_tile, direction, tunnel_length

        return None, None, None, None, None

    def add_room(self, room_x, room_y, room):
        room_width, room_height = self.get_room_dimensions(room)
        for x in range(room_width):
            for y in range(room_height):
                if not room[x][y].block_path:
                    self.level[int(room_x + x)][int(room_y + y)] = Tile(False, False)

        self.rooms.append(room)

    def add_tunnel(self, wall_tile, direction, tunnel_length):
        start_x = wall_tile[0] + direction[0] * tunnel_length
        start_y = wall_tile[1] + direction[1] * tunnel_length

        for i in range(self.max_tunnel_length):
            x = start_x - direction[0] * i
            y = start_y - direction[1] * i
            self.level[x][y] = Tile(False, False)

            if ((x + direction[0]) == wall_tile[0] and
                    (y + direction[1]) == wall_tile[1]):
                break

    def get_room_dimensions(self, room):
        if room:
            room_width = len(room)
            room_height = len(room[0])
            return room_width, room_height
        else:
            room_width = 0
            room_height = 0
            return room_width, room_height

    def get_adjacent_walls(self, tile_x, tile_y, room):
        wall_counter = 0
        for x in range(tile_x - 1, tile_x + 2):
            for y in range(tile_y - 1, tile_y + 2):
                if room[x][y].block_path:
                    if (x != tile_x) or (y != tile_y):
                        wall_counter += 1
        return wall_counter

    def get_direction(self):
        north = (0, -1)
        south = (0, 1)
        east = (1, 0)
        west = (-1, 0)

        direction = random.choice([north, south, east, west])
        return direction

    def get_overlap(self, room, room_x, room_y):
        room_width, room_height = self.get_room_dimensions(room)
        for x in range(room_width):
            for y in range(room_height):
                if not room[x][y].block_path:
                    if ((1 <= (x + room_x) < MAPWIDTH - 1) and
                            (1 <= (y + room_y) < MAPHEIGHT - 1)):
                        # Check for overlap with a one tile buffer
                        if not self.level[x + room_x - 1][y + room_y - 1].block_path:  # top left
                            return False
                        if not self.level[x + room_x][y + room_y - 1].block_path:  # top center
                            return False
                        if not self.level[x + room_x + 1][y + room_y - 1].block_path:  # top right
                            return False

                        if not self.level[x + room_x - 1][y + room_y].block_path:  # left
                            return False
                        if not self.level[x + room_x][y + room_y].block_path:  # center
                            return False
                        if not self.level[x + room_x + 1][y + room_y].block_path:  # right
                            return False

                        if not self.level[x + room_x - 1][y + room_y + 1].block_path:  # bottom left
                            return False
                        if not self.level[x + room_x][y + room_y + 1].block_path:  # bottom center
                            return False
                        if not self.level[x + room_x + 1][y + room_y + 1].block_path:  # bottom right
                            return False

                    else:  # room is out of bounds
                        return False

    def add_shortcuts(self):
        libtcod_map = libtcod.map_new(MAPWIDTH, MAPHEIGHT)
        self.recomputepath_map(libtcod_map)

        for i in range(self.shortcut_attempts):
            while True:
                floor_x = random.randint(self.shortcut_length + 1, (MAPWIDTH - self.shortcut_length - 1))
                floor_y = random.randint(self.shortcut_length + 1, (MAPHEIGHT - self.shortcut_length - 1))
                if not self.level[floor_x][floor_y].block_path:
                    if (self.level[floor_x - 1][floor_y].block_path or
                            self.level[floor_x + 1][floor_y].block_path or
                            self.level[floor_x][floor_y - 1].block_path or
                            self.level[floor_x][floor_y + 1].block_path):
                        break

            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:
                        new_x = floor_x + (x * self.shortcut_length)
                        new_y = floor_y + (y * self.shortcut_length)
                        if not self.level[x][y].block_path:
                            path_map = libtcod.path_new_using_map(libtcod_map)
                            libtcod.path_compute(path_map, floor_x, floor_y, new_x, new_y)
                            distance = libtcod.path_size(path_map)

                            if distance > self.min_pathfinding_distance:
                                self.carve_shortcut(floor_x, floor_y, new_x, new_y)
                                self.recomputepath_map(libtcod_map)

        libtcod.path_delete(path_map)

    def recomputepath_map(self, libtcod_map):
        for x in range(MAPWIDTH):
            for y in range(MAPWIDTH):
                if self.level[x][y].block_path:
                    libtcod.map_set_properties(libtcod_map, x, y, False, False)
                else:
                    libtcod.map_set_properties(libtcod_map, x, y, True, True)

    def carve_shortcut(self, x1, y1, x2, y2):
        if x1 - x2 == 0:
            # Carve virtical tunnel
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.level[x1][y] = Tile(False, False)

        elif y1 - y2 == 0:
            # Carve Horizontal tunnel
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.level[x][y1] = Tile(False, False)

        elif (y1 - y2) / (x1 - x2) == 1:
            # Carve NW to SE Tunnel
            x = min(x1, x2)
            y = min(y1, y2)
            while x != max(x1, x2):
                x += 1
                self.level[x][y] = Tile(False, False)
                y += 1
                self.level[x][y] = Tile(False, False)

        elif (y1 - y2) / (x1 - x2) == -1:
            # Carve NE to SW Tunnel
            x = min(x1, x2)
            y = max(y1, y2)
            while x != max(x1, x2):
                x += 1
                self.level[x][y] = Tile(False, False)
                y -= 1
                self.level[x][y] = Tile(False, False)

    def check_room_exists(self, room):
        room_width, room_height = self.get_room_dimensions(room)
        for x in range(room_width):
            for y in range(room_height):
                if room[x][y] == 0:
                    return True
        return False






































