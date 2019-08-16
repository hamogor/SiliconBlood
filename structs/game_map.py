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
        self.map = MessyBSPTree().generateLevel(GRIDWIDTH, GRIDHEIGHT)
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


class MessyBSPTree:
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
        self.smoothEdges = True
        self.smoothing = 1
        self.filling = 3

    def generateLevel(self, mapWidth, mapHeight):
        # Creates an empty 2D array or clears existing array
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.level = [[1
                       for y in range(mapHeight)]
                      for x in range(mapWidth)]

        self._leafs = []

        rootLeaf = Leaf(0, 0, mapWidth, mapHeight)
        self._leafs.append(rootLeaf)

        splitSuccessfully = True
        # loop through all leaves until they can no longer split successfully
        while splitSuccessfully:
            splitSuccessfully = False
            for l in self._leafs:
                if l.child_1 == None and l.child_2 == None:
                    if ((l.width > self.MAX_LEAF_SIZE) or
                            (l.height > self.MAX_LEAF_SIZE) or
                            (random.random() > 0.8)):
                        if l.splitLeaf():  # try to split the leaf
                            self._leafs.append(l.child_1)
                            self._leafs.append(l.child_2)
                            splitSuccessfully = True

        rootLeaf.createRooms(self)
        self.cleanUpMap(mapWidth, mapHeight)

        return self.level

    def createRoom(self, room):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y] = 0

    def createHall(self, room1, room2):
        # run a heavily weighted random Walk
        # from point2 to point1
        drunkardX, drunkardY = room2.center()
        goalX, goalY = room1.center()
        while not (room1.x1 <= drunkardX <= room1.x2) or not (room1.y1 < drunkardY < room1.y2):  #
            # ==== Choose Direction ====
            north = 1.0
            south = 1.0
            east = 1.0
            west = 1.0

            weight = 1

            # weight the random walk against edges
            if drunkardX < goalX:  # drunkard is left of point1
                east += weight
            elif drunkardX > goalX:  # drunkard is right of point1
                west += weight
            if drunkardY < goalY:  # drunkard is above point1
                south += weight
            elif drunkardY > goalY:  # drunkard is below point1
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
            # check colision at edges
            if (0 < drunkardX + dx < self.mapWidth - 1) and (0 < drunkardY + dy < self.mapHeight - 1):
                drunkardX += dx
                drunkardY += dy
                if self.level[int(drunkardX)][int(drunkardY)] == 1:
                    self.level[int(drunkardX)][int(drunkardY)] = 0

    def cleanUpMap(self, mapWidth, mapHeight):
        if (self.smoothEdges):
            for i in range(3):
                # Look at each cell individually and check for smoothness
                for x in range(1, mapWidth - 1):
                    for y in range(1, mapHeight - 1):
                        if (self.level[x][y] == 1) and (self.getAdjacentWallsSimple(x, y) <= self.smoothing):
                            self.level[x][y] = 0

                        if (self.level[x][y] == 0) and (self.getAdjacentWallsSimple(x, y) >= self.filling):
                            self.level[x][y] = 1

    def getAdjacentWallsSimple(self, x, y):  # finds the walls in four directions
        wallCounter = 0
        # print("(",x,",",y,") = ",self.level[x][y])
        if self.level[x][y - 1] == 1:  # Check north
            wallCounter += 1
        if self.level[x][y + 1] == 1:  # Check south
            wallCounter += 1
        if self.level[x - 1][y] == 1:  # Check west
            wallCounter += 1
        if self.level[x + 1][y] == 1:  # Check east
            wallCounter += 1

        return wallCounter


# ==== TinyKeep ====
'''
https://www.reddit.com/r/gamedev/comments/1dlwc4/procedural_dungeon_generation_algorithm_explained/
and
http://www.gamasutra.com/blogs/AAdonaac/20150903/252889/Procedural_Dungeon_Generation_Algorithm.php
'''


# ==== Helper Classes ====
class Rect:  # used for the tunneling algorithm
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        centerX = (self.x1 + self.x2) / 2
        centerY = (self.y1 + self.y2) / 2
        return centerX, centerY

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
        self.hall = None

    def splitLeaf(self):
        # begin splitting the leaf into two children
        if self.child_1 != None or self.child_2 != None:
            return False  # This leaf has already been split

        '''
        ==== Determine the direction of the split ====
        If the width of the leaf is >25% larger than the height,
        split the leaf vertically.
        If the height of the leaf is >25 larger than the width,
        split the leaf horizontally.
        Otherwise, choose the direction at random.
        '''
        splitHorizontally = random.choice([True, False])
        if self.width / self.height >= 1.25:
            splitHorizontally = False
        elif self.height / self.width >= 1.25:
            splitHorizontally = True

        if splitHorizontally:
            max = self.height - self.MIN_LEAF_SIZE
        else:
            max = self.width - self.MIN_LEAF_SIZE

        if max <= self.MIN_LEAF_SIZE:
            return False  # the leaf is too small to split further

        split = random.randint(self.MIN_LEAF_SIZE, max)  # determine where to split the leaf

        if splitHorizontally:
            self.child_1 = Leaf(self.x, self.y, self.width, split)
            self.child_2 = Leaf(self.x, self.y + split, self.width, self.height - split)
        else:
            self.child_1 = Leaf(self.x, self.y, split, self.height)
            self.child_2 = Leaf(self.x + split, self.y, self.width - split, self.height)

        return True

    def createRooms(self, bspTree):
        if self.child_1 or self.child_2:
            # recursively search for children until you hit the end of the branch
            if self.child_1:
                self.child_1.createRooms(bspTree)
            if self.child_2:
                self.child_2.createRooms(bspTree)

            if self.child_1 and self.child_2:
                bspTree.createHall(self.child_1.getRoom(),
                                   self.child_2.getRoom())

        else:
            # Create rooms in the end branches of the bsp tree
            w = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE, self.width - 1))
            h = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE, self.height - 1))
            x = random.randint(self.x, self.x + (self.width - 1) - w)
            y = random.randint(self.y, self.y + (self.height - 1) - h)
            self.room = Rect(x, y, w, h)
            bspTree.createRoom(self.room)

    def getRoom(self):
        if self.room:
            return self.room

        else:
            if self.child_1:
                self.room_1 = self.child_1.getRoom()
            if self.child_2:
                self.room_2 = self.child_2.getRoom()

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
