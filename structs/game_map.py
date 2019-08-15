import tcod as libtcod
from settings import GRIDWIDTH, GRIDHEIGHT, S_WALL, S_FLOOR, S_STAIRS
import random
from utils.map_utils import check_for_wall
from structs.tile import Tile
from structs.assets import Assets


class GameMap:
    '''
    What I'm calling the Room Addition algorithm is an attempt to
    recreate the dungeon generation algorithm used in Brogue, as
    discussed at https://www.rockpapershotgun.com/2015/07/28/how-do-roguelikes-generate-levels/
    I don't think Brian Walker has ever given a name to his
    dungeon generation algorithm, so I've taken to calling it the
    Room Addition Algorithm, after the way in which it builds the
    dungeon by adding rooms one at a time to the existing dungeon.
    This isn't a perfect recreation of Brian Walker's algorithm,
    but I think it's good enough to demonstrait the concept.
    '''

    def __init__(self):
        self.level = []

        self.ROOM_MAX_SIZE = 18  # max height and width for cellular automata rooms
        self.ROOM_MIN_SIZE = 16  # min size in number of floor tiles, not height and width
        self.MAX_NUM_ROOMS = 30

        self.SQUARE_ROOM_MAX_SIZE = 12
        self.SQUARE_ROOM_MIN_SIZE = 6

        self.CROSS_ROOM_MAX_SIZE = 12
        self.CROSS_ROOM_MIN_SIZE = 6

        self.cavern_chance = 0.40  # probability that the first room will be a cavern
        self.CAVERN_MAX_SIZE = 16  # max height an width

        self.wall_probability = 0.45
        self.neighbors = 4

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
        self.map = self.generate_level()
        self.tiles = [[Tile(True, True)
                       for _ in range(GRIDHEIGHT)]
                      for _ in range(GRIDWIDTH)]
        for x in range(GRIDWIDTH):
            for y in range(GRIDHEIGHT):
                if self.map[x][y] == 1:
                    self.tiles[x][y] = Tile(True, True, S_WALL)
                else:
                    self.tiles[x][y] = Tile(False, False, S_FLOOR)

        self.assign_tiles()
        self.place_stairs()
        self.tiles[5][5] = Tile(False, False, S_STAIRS, "stairs")

    def place_stairs(self):
        x = random.randint(0, GRIDWIDTH - 1)
        y = random.randint(0, GRIDHEIGHT - 1)

        if not self.tiles[x][y].block_path:
            self.tiles[x][y] = Tile(False, False, S_STAIRS, "stairs")
        else:
            self.place_stairs()

    def generate_level(self):
        
        map_width = GRIDWIDTH
        map_height = GRIDHEIGHT

        self.level = [[1
                       for y in range(GRIDHEIGHT)]
                      for x in range(GRIDWIDTH)]

        # generate the first room
        room = self.generate_room()
        room_width, room_height = self.get_room_dimensions(room)
        room_x = (map_width / 2 - room_width / 2) - 1
        room_y = (map_height / 2 - room_height / 2) - 1
        self.add_room(room_x, room_y, room)

        # generate other rooms
        for i in range(self.build_room_attempts):
            room = self.generate_room()
            # try to position the room, get room_x and room_y
            room_x, room_y, wall_tile, direction, tunnel_length = self.place_room(room, map_width, map_height)
            if room_x and room_y:
                self.add_room(room_x, room_y, room)
                self.add_tunnel(wall_tile, direction, tunnel_length)
                if len(self.rooms) >= self.MAX_NUM_ROOMS:
                    break

        if self.include_shortcuts:
            self.add_shortcuts(GRIDWIDTH, GRIDHEIGHT)
        return self.level

    def assign_tiles(self):
        # loop through map looking for the walls, then assign bitoperator
        assets = Assets()
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[0])):

                # check tile for wall status
                tile_is_wall = check_for_wall(x, y, self.tiles)

                if tile_is_wall:
                    # create tile var
                    tile_assignment = 0
                    # add bitmask value
                    if check_for_wall(x, y - 1, self.tiles):
                        tile_assignment += 1
                    if check_for_wall(x + 1, y, self.tiles):
                        tile_assignment += 2
                    if check_for_wall(x, y + 1, self.tiles):
                        tile_assignment += 4
                    if check_for_wall(x - 1, y, self.tiles):
                        tile_assignment += 8
                    self.tiles[x][y].sprite = assets.wall_dict[tile_assignment]
                    self.tiles[x][y].assignment = tile_assignment

    def generate_room(self):
        # select a room type to generate
        # generate and return that room
        if self.rooms:
            # There is at least one room already
            choice = random.random()

            if choice < self.square_room_chance:
                room = self.generate_room_square()
            elif self.square_room_chance <= choice < (self.square_room_chance + self.cross_room_chance):
                room = self.generate_room_cross()
            else:
                room = self.generate_room_ca()

        else:  # it's the first room
            choice = random.random()
            if choice < self.cavern_chance:
                room = self.generate_room_cavern()
            else:
                room = self.generate_room_square()

        return room

    def generate_room_cross(self):
        room_hor_width = (random.randint(self.CROSS_ROOM_MIN_SIZE + 2, self.CROSS_ROOM_MAX_SIZE)) / 2 * 2

        room_vir_height = (random.randint(self.CROSS_ROOM_MIN_SIZE + 2, self.CROSS_ROOM_MAX_SIZE)) / 2 * 2

        room_hor_height = (random.randint(self.CROSS_ROOM_MIN_SIZE, room_vir_height - 2)) / 2 * 2

        room_vir_width = (random.randint(self.CROSS_ROOM_MIN_SIZE, room_hor_width - 2)) / 2 * 2

        room = [[1
                 for y in range(int(room_vir_height))]
                for x in range(int(room_hor_width))]

        # Fill in horizontal space
        vir_offset = room_vir_height / 2 - room_hor_height / 2
        for y in range(int(vir_offset), int(room_hor_height + vir_offset)):
            for x in range(0, int(room_hor_width)):
                room[x][y] = 0

        # Fill in vertical space
        hor_offset = room_hor_width / 2 - room_vir_width / 2
        for y in range(0, int(room_vir_height)):
            for x in range(int(hor_offset), int(room_vir_width + hor_offset)):
                room[x][y] = 0

        return room

    def generate_room_square(self):
        room_width = random.randint(self.SQUARE_ROOM_MIN_SIZE, self.SQUARE_ROOM_MAX_SIZE)
        room_height = random.randint(max(int(room_width * 0.5), self.SQUARE_ROOM_MIN_SIZE),
                                     min(int(room_width * 1.5), self.SQUARE_ROOM_MAX_SIZE))

        room = [[1
                 for y in range(room_height)]
                for x in range(room_width)]

        room = [[0
                 for y in range(1, room_height - 1)]
                for x in range(1, room_width - 1)]

        return room

    def generate_room_ca(self):
        while True:
            # if a room is too small, generate another
            room = [[1
                     for y in range(self.ROOM_MAX_SIZE)]
                    for x in range(self.ROOM_MAX_SIZE)]

            # random fill map
            for y in range(2, self.ROOM_MAX_SIZE - 2):
                for x in range(2, self.ROOM_MAX_SIZE - 2):
                    if random.random() >= self.wall_probability:
                        room[x][y] = 0

            # create distinctive regions
            for i in range(4):
                for y in range(1, self.ROOM_MAX_SIZE - 1):
                    for x in range(1, self.ROOM_MAX_SIZE - 1):

                        # if the cell's neighboring walls > self.neighbors, set it to 1
                        if self.get_adjacent_walls(x, y, room) > self.neighbors:
                            room[x][y] = 1
                        # otherwise, set it to 0
                        elif self.get_adjacent_walls(x, y, room) < self.neighbors:
                            room[x][y] = 0

            # flood_fill to remove small caverns
            room = self.flood_fill(room)

            # start over if the room is completely filled in
            room_width, room_height = self.get_room_dimensions(room)
            for x in range(room_width):
                for y in range(room_height):
                    if room[x][y] == 0:
                        return room

    def generate_room_cavern(self):
        while True:
            # if a room is too small, generate another
            room = [[1
                     for y in range(self.CAVERN_MAX_SIZE)]
                    for x in range(self.CAVERN_MAX_SIZE)]

            # random fill map
            for y in range(2, self.CAVERN_MAX_SIZE - 2):
                for x in range(2, self.CAVERN_MAX_SIZE - 2):
                    if random.random() >= self.wall_probability:
                        room[x][y] = 0

            # create distinctive regions
            for i in range(4):
                for y in range(1, self.CAVERN_MAX_SIZE - 1):
                    for x in range(1, self.CAVERN_MAX_SIZE - 1):

                        # if the cell's neighboring walls > self.neighbors, set it to 1
                        if self.get_adjacent_walls(x, y, room) > self.neighbors:
                            room[x][y] = 1
                        # otherwise, set it to 0
                        elif self.get_adjacent_walls(x, y, room) < self.neighbors:
                            room[x][y] = 0

            # flood_fill to remove small caverns
            room = self.flood_fill(room)

            # start over if the room is completely filled in
            room_width, room_height = self.get_room_dimensions(room)
            for x in range(room_width):
                for y in range(room_height):
                    if room[x][y] == 0:
                        return room

    def flood_fill(self, room):
        '''
        Find the largest region. Fill in all other regions.
        '''
        room_width, room_height = self.get_room_dimensions(room)
        largest_region = set()

        for x in range(room_width):
            for y in range(room_height):
                if room[x][y] == 0:
                    new_region = set()
                    tile = (x, y)
                    to_be_filled = set([tile])
                    while to_be_filled:
                        tile = to_be_filled.pop()

                        if tile not in new_region:
                            new_region.add(tile)

                            room[tile[0]][tile[1]] = 1

                            # check adjacent cells
                            x = tile[0]
                            y = tile[1]
                            north = (x, y - 1)
                            south = (x, y + 1)
                            east = (x + 1, y)
                            west = (x - 1, y)

                            for direction in [north, south, east, west]:

                                if room[direction[0]][direction[1]] == 0:
                                    if direction not in to_be_filled and direction not in new_region:
                                        to_be_filled.add(direction)

                    if len(new_region) >= self.ROOM_MIN_SIZE:
                        if len(new_region) > len(largest_region):
                            largest_region.clear()
                            largest_region.update(new_region)

        for tile in largest_region:
            room[tile[0]][tile[1]] = 0

        return room

    def place_room(self, room, map_width, map_height):  # (self,room,direction,)
        room_x = None
        room_y = None

        room_width, room_height = self.get_room_dimensions(room)

        # try n times to find a wall that lets you build room in that direction
        for i in range(self.place_room_attempts):
            # try to place the room against the tile, else connected by a tunnel of length i

            wall_tile = None
            direction = self.get_direction()
            while not wall_tile:
                '''
                randomly select tiles until you find
                a wall that has another wall in the
                chosen direction and has a floor in the 
                opposite direction.
                '''
                # direction == tuple(dx,dy)
                tile_x = random.randint(1, map_width - 2)
                tile_y = random.randint(1, map_height - 2)
                if ((self.level[tile_x][tile_y] == 1) and
                        (self.level[tile_x + direction[0]][tile_y + direction[1]] == 1) and
                        (self.level[tile_x - direction[0]][tile_y - direction[1]] == 0)):
                    wall_tile = (tile_x, tile_y)

            # spawn the room touching wall_tile
            startroom_x = None
            startroom_y = None
            '''
            replace this with a method that returns a 
            random floor tile instead of the top left floor tile
            '''
            while not startroom_x and not startroom_y:
                x = random.randint(0, room_width - 1)
                y = random.randint(0, room_height - 1)
                if room[x][y] == 0:
                    startroom_x = wall_tile[0] - x
                    startroom_y = wall_tile[1] - y

            # then slide it until it doesn't touch anything
            for tunnel_length in range(self.max_tunnel_length):
                possibleroom_x = startroom_x + direction[0] * tunnel_length
                possibleroom_y = startroom_y + direction[1] * tunnel_length

                enough_room = self.get_overlap(room, possibleroom_x, possibleroom_y, map_width, map_height)

                if enough_room:
                    room_x = possibleroom_x
                    room_y = possibleroom_y

                    # build connecting tunnel
                    # Attempt 1
                    '''
                    for i in range(tunnel_length+1):
                        x = wall_tile[0] + direction[0]*i
                        y = wall_tile[1] + direction[1]*i
                        self.level[x][y] = 0
                    '''
                    # moved tunnel code into self.generate_level()

                    return room_x, room_y, wall_tile, direction, tunnel_length

        return None, None, None, None, None

    def add_room(self, room_x, room_y, room):
        room_width, room_height = self.get_room_dimensions(room)
        for x in range(room_width):
            for y in range(room_height):
                if room[x][y] == 0:
                    self.level[int(room_x + x)][int(room_y + y)] = 0

        self.rooms.append(room)

    def add_tunnel(self, wall_tile, direction, tunnel_length):
        # carve a tunnel from a point in the room back to
        # the wall tile that was used in its original placement

        start_x = wall_tile[0] + direction[0] * tunnel_length
        start_y = wall_tile[1] + direction[1] * tunnel_length
        # self.level[start_x][start_y] = 1

        for i in range(self.max_tunnel_length):
            x = start_x - direction[0] * i
            y = start_y - direction[1] * i
            self.level[x][y] = 0
            # If you want doors, this is where the code should go
            if ((x + direction[0]) == wall_tile[0] and
                    (y + direction[1]) == wall_tile[1]):
                break

    @staticmethod
    def get_room_dimensions(room):
        if room:
            room_width = len(room)
            room_height = len(room[0])
            return room_width, room_height
        else:
            room_width = 0
            room_height = 0
            return room_width, room_height

    @staticmethod
    def get_adjacent_walls(tile_x, tile_y, room):  # finds the walls in 8 directions
        wall_counter = 0
        for x in range(tile_x - 1, tile_x + 2):
            for y in range(tile_y - 1, tile_y + 2):
                if room[x][y] == 1:
                    if (x != tile_x) or (y != tile_y):  # exclude (tile_x,tile_y)
                        wall_counter += 1
        return wall_counter

    @staticmethod
    def get_direction():
        # direction = (dx,dy)
        north = (0, -1)
        south = (0, 1)
        east = (1, 0)
        west = (-1, 0)

        direction = random.choice([north, south, east, west])
        return direction

    def get_overlap(self, room, room_x, room_y, map_width, map_height):
        '''
        for each 0 in room, check the cooresponding tile in
        self.level and the eight tiles around it. Though slow,
        that should insure that there is a wall between each of
        the rooms created in this way.
        <> check for overlap with self.level
        <> check for out of bounds
        '''
        room_width, room_height = self.get_room_dimensions(room)
        for x in range(room_width):
            for y in range(room_height):
                if room[x][y] == 0:
                    # Check to see if the room is out of bounds
                    if ((1 <= (x + room_x) < map_width - 1) and
                            (1 <= (y + room_y) < map_height - 1)):
                        # Check for overlap with a one tile buffer
                        if self.level[x + room_x - 1][y + room_y - 1] == 0:  # top left
                            return False
                        if self.level[x + room_x][y + room_y - 1] == 0:  # top center
                            return False
                        if self.level[x + room_x + 1][y + room_y - 1] == 0:  # top right
                            return False

                        if self.level[x + room_x - 1][y + room_y] == 0:  # left
                            return False
                        if self.level[x + room_x][y + room_y] == 0:  # center
                            return False
                        if self.level[x + room_x + 1][y + room_y] == 0:  # right
                            return False

                        if self.level[x + room_x - 1][y + room_y + 1] == 0:  # bottom left
                            return False
                        if self.level[x + room_x][y + room_y + 1] == 0:  # bottom center
                            return False
                        if self.level[x + room_x + 1][y + room_y + 1] == 0:  # bottom right
                            return False

                    else:  # room is out of bounds
                        return False
        return True

    def add_shortcuts(self, map_width, map_height):
        '''
        I use libtcodpy's built in pathfinding here, since I'm
        already using libtcodpy for the iu. At the moment,
        the way I find the distance between
        two points to see if I should put a shortcut there
        is horrible, and its easily the slowest part of this
        algorithm. If I think of a better way to do this in
        the future, I'll implement it.
        '''

        # initialize the libtcodpy map
        libtcod_map = libtcod.map_new(map_width, map_height)
        self.recomputepath_map(map_width, map_height, libtcod_map)

        for i in range(self.shortcut_attempts):
            # check i times for places where shortcuts can be made
            while True:
                # Pick a random floor tile
                floor_x = random.randint(self.shortcut_length + 1, (map_width - self.shortcut_length - 1))
                floor_y = random.randint(self.shortcut_length + 1, (map_height - self.shortcut_length - 1))
                if self.level[floor_x][floor_y] == 0:
                    if (self.level[floor_x - 1][floor_y] == 1 or
                            self.level[floor_x + 1][floor_y] == 1 or
                            self.level[floor_x][floor_y - 1] == 1 or
                            self.level[floor_x][floor_y + 1] == 1):
                        break

            # look around the tile for other floor tiles
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:  # Exclude the center tile
                        new_x = floor_x + (x * self.shortcut_length)
                        new_y = floor_y + (y * self.shortcut_length)
                        if self.level[new_x][new_y] == 0:
                            # run pathfinding algorithm between the two points
                            # back to the libtcodpy nonesense
                            path_map = libtcod.path_new_using_map(libtcod_map)
                            libtcod.path_compute(path_map, floor_x, floor_y, new_x, new_y)
                            distance = libtcod.path_size(path_map)

                            if distance > self.min_pathfinding_distance:
                                # make shortcut
                                self.carve_shortcut(floor_x, floor_y, new_x, new_y)
                                self.recomputepath_map(map_width, map_height, libtcod_map)

        # destroy the path object
        libtcod.path_delete(path_map)

    def recomputepath_map(self, map_width, map_height, libtcod_map):
        for x in range(map_width):
            for y in range(map_height):
                if self.level[x][y] == 1:
                    libtcod.map_set_properties(libtcod_map, x, y, False, False)
                else:
                    libtcod.map_set_properties(libtcod_map, x, y, True, True)

    def carve_shortcut(self, x1, y1, x2, y2):
        if x1 - x2 == 0:
            # Carve vertical tunnel
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.level[x1][y] = 0

        elif y1 - y2 == 0:
            # Carve Horizontal tunnel
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.level[x][y1] = 0

        elif (y1 - y2) / (x1 - x2) == 1:
            # Carve NW to SE Tunnel
            x = min(x1, x2)
            y = min(y1, y2)
            while x != max(x1, x2):
                x += 1
                self.level[x][y] = 0
                y += 1
                self.level[x][y] = 0

        elif (y1 - y2) / (x1 - x2) == -1:
            # Carve NE to SW Tunnel
            x = min(x1, x2)
            y = max(y1, y2)
            while x != max(x1, x2):
                x += 1
                self.level[x][y] = 0
                y -= 1
                self.level[x][y] = 0

    def check_room_exists(self, room):
        room_width, room_height = self.get_room_dimensions(room)
        for x in range(room_width):
            for y in range(room_height):
                if room[x][y] == 0:
                    return True
        return False
