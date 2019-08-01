class RoomAddition:

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
        self.CAVERN_MAX_SIZE = 35  # max height an width

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
        self.tiles = self.generate_level()

    def generate_level(self):

        self.level = [[1
                       for y in range(GRIDHEIGHT)]
                      for x in range(GRIDWIDTH)]

        self.tiles = [[StrucTile(True, True) for y in range(GRIDHEIGHT)] for x in range(GRIDWIDTH)]

        # generate the first room
        room = self.generate_room()
        room_width, room_height = self.get_room_dimensions(room)
        room_x = (GRIDWIDTH / 2 - room_width / 2) - 1
        room_y = (GRIDHEIGHT / 2 - room_height / 2) - 1
        self.add_room(room_x, room_y, room)

        # generate other rooms
        for i in range(self.build_room_attempts):
            room = self.generate_room()
            # try to position the room, get room_x and room_y
            room_x, room_y, wall_tile, direction, tunnel_length = self.place_room(room, GRIDWIDTH, GRIDHEIGHT)
            if room_x and room_y:
                self.add_room(room_x, room_y, room)
                self.add_tunnel(wall_tile, direction, tunnel_length)
                if len(self.rooms) >= self.MAX_NUM_ROOMS:
                    break

        if self.include_shortcuts:
            self.add_shortcuts(GRIDWIDTH, GRIDHEIGHT)

        return self.tiles

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
        room_h_width = (random.randint(self.CROSS_ROOM_MIN_SIZE + 2, self.CROSS_ROOM_MAX_SIZE)) / 2 * 2

        room_vir_height = (random.randint(self.CROSS_ROOM_MIN_SIZE + 2, self.CROSS_ROOM_MAX_SIZE)) / 2 * 2

        room_hor_height = (random.randint(self.CROSS_ROOM_MIN_SIZE, room_vir_height - 2)) / 2 * 2

        room_vir_width = (random.randint(self.CROSS_ROOM_MIN_SIZE, room_h_width - 2)) / 2 * 2

        room = [[1
                 for y in range(int(room_vir_height))]
                for x in range(int(room_h_width))]

        # Fill in horizontal space
        vir_offset = room_vir_height / 2 - room_hor_height / 2
        for y in range(int(vir_offset), int(room_hor_height) + int(vir_offset)):
            for x in range(0, int(room_h_width)):
                room[int(x)][int(y)] = 0

        # Fill in virtical space
        hor_offset = int(room_h_width / 2) - int(room_vir_width / 2)
        for y in range(0, int(room_vir_height)):
            for x in range(int(hor_offset), int(room_vir_width + hor_offset)):
                room[int(x)][int(y)] = 0
                self.set_tile(False, x, y)

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
                        self.set_tile(False, x, y)

            # create distinctive regions
            for i in range(4):
                for y in range(1, self.ROOM_MAX_SIZE - 1):
                    for x in range(1, self.ROOM_MAX_SIZE - 1):

                        # if the cell's neighboring walls > self.neighbors, set it to 1
                        if self.get_adjacent_walls(x, y, room) > self.neighbors:
                            room[x][y] = 1
                            self.set_tile(True, x, y)
                        # otherwise, set it to 0
                        elif self.get_adjacent_walls(x, y, room) < self.neighbors:
                            room[x][y] = 0
                            self.set_tile(True, x, y)

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
                            self.set_tile(True, x, y)
                        # otherwise, set it to 0
                        elif self.get_adjacent_walls(x, y, room) < self.neighbors:
                            room[x][y] = 0
                            self.set_tile(False, x, y)

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
                            self.set_tile(True, tile[0], tile[1])

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
            self.set_tile(False, tile[0], tile[1])

        return room

    def place_room(self, room, GRIDWIDTH, GRIDHEIGHT):  # (self,room,direction,)
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
                tile_x = random.randint(1, GRIDWIDTH - 2)
                tile_y = random.randint(1, GRIDHEIGHT - 2)
                if ((self.level[tile_x][tile_y] == 1) and
                        (self.level[tile_x + direction[0]][tile_y + direction[1]] == 1) and
                        (self.level[tile_x - direction[0]][tile_y - direction[1]] == 0)):
                    wall_tile = (tile_x, tile_y)

            # spawn the room touching wall_tile
            startroom_x = None
            startroom_y = None
            '''
            TODO: replace this with a method that returns a 
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

                enough_room = self.getOverlap(room, possibleroom_x, possibleroom_y, GRIDWIDTH, GRIDHEIGHT)

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
                    self.set_tile(False, room_x + x, room_y + y)

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
            self.set_tile(False, x, y)
            # If you want doors, this is where the code should go
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

    def get_adjacent_walls(self, tile_x, tile_y, room):  # finds the walls in 8 directions
        wall_counter = 0
        for x in range(tile_x - 1, tile_x + 2):
            for y in range(tile_y - 1, tile_y + 2):
                if room[x][y] == 1:
                    if (x != tile_x) or (y != tile_y):  # exclude (tile_x,tile_y)
                        wall_counter += 1
        return wall_counter

    def get_direction(self):
        # direction = (dx,dy)
        north = (0, -1)
        south = (0, 1)
        east = (1, 0)
        west = (-1, 0)

        direction = random.choice([north, south, east, west])
        return direction

    def getOverlap(self, room, room_x, room_y, GRIDWIDTH, GRIDHEIGHT):
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
                    if ((1 <= (x + room_x) < GRIDWIDTH - 1) and
                            (1 <= (y + room_y) < GRIDHEIGHT - 1)):
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

    def add_shortcuts(self, GRIDWIDTH, GRIDHEIGHT):
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
        libtcod_map = libtcod.map_new(GRIDWIDTH, GRIDHEIGHT)
        self.recomputepath_map(GRIDWIDTH, GRIDHEIGHT, libtcod_map)

        for i in range(self.shortcut_attempts):
            # check i times for places where shortcuts can be made
            while True:
                # Pick a random floor tile
                floor_x = random.randint(self.shortcut_length + 1, (GRIDWIDTH - self.shortcut_length - 1))
                floor_y = random.randint(self.shortcut_length + 1, (GRIDHEIGHT - self.shortcut_length - 1))
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
                                self.recomputepath_map(GRIDWIDTH, GRIDHEIGHT, libtcod_map)

        # destroy the path object
        libtcod.path_delete(path_map)

    def recomputepath_map(self, GRIDWIDTH, GRIDHEIGHT, libtcod_map):
        for x in range(GRIDWIDTH):
            for y in range(GRIDHEIGHT):
                if self.level[x][y] == 1:
                    libtcod.map_set_properties(libtcod_map, x, y, False, False)
                else:
                    libtcod.map_set_properties(libtcod_map, x, y, True, True)

    def carve_shortcut(self, x1, y1, x2, y2):
        if x1 - x2 == 0:
            # Carve virtical tunnel
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.level[x1][y] = 0
                self.set_tile(False, x1, y1)

        elif y1 - y2 == 0:
            # Carve Horizontal tunnel
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.level[x][y1] = 0
                self.set_tile(False, x, y1)

        elif (y1 - y2) / (x1 - x2) == 1:
            # Carve NW to SE Tunnel
            x = min(x1, x2)
            y = min(y1, y2)
            while x != max(x1, x2):
                x += 1
                self.level[x][y] = 0
                self.set_tile(False, x, y)
                y += 1
                self.level[x][y] = 0
                self.set_tile(False, x, y)

        elif (y1 - y2) / (x1 - x2) == -1:
            # Carve NE to SW Tunnel
            x = min(x1, x2)
            y = max(y1, y2)
            while x != max(x1, x2):
                x += 1
                self.level[x][y] = 0
                self.set_tile(False, x, y)
                y -= 1
                self.level[x][y] = 0
                self.set_tile(False, x, y)

    def check_room_exists(self, room):
        room_width, room_height = self.get_room_dimensions(room)
        for x in range(room_width):
            for y in range(room_height):
                if room[x][y] == 0:
                    return True
        return False

    def set_tile(self, blocks, x, y):
        if blocks:
            self.tiles[int(x)][int(y)].block_path = True
            self.tiles[int(x)][int(y)].block_path = True
            self.tiles[int(x)][int(y)].sprite = S_WALL
            self.tiles[int(x)][int(y)].dark_sprite = S_DWALL
        else:
            self.tiles[int(x)][int(y)].block_path = False
            self.tiles[int(x)][int(y)].block_path = False
            self.tiles[int(x)][int(y)].sprite = S_FLOOR
            self.tiles[int(x)][int(y)].dark_sprite = S_DFLOOR

class GameMap:
    def __init__(self):
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self.list_rooms = []
        self.list_regions = []
        self.list_objects = []
        self.room = None
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self._leafs = []
        self.MAX_LEAF_SIZE = 35
        self.ROOM_MAX_SIZE = 25
        self.ROOM_MIN_SIZE = 8
        self.level = []
        self.first_room = False
        #self.tiles = self.generate_level()
        self.messyBSPTree = MessyBSPTree()
        self.tiles = self.messyBSPTree.generate_level(GRIDWIDTH, GRIDHEIGHT)
        #self.place_stairs()

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

    def place_stairs(self):
        last_room = self._leafs[-1]
        stair_pos = self.tiles[last_room.room.center()[0]][last_room.room.center()[1]]
        stair_pos.sprite = S_STAIRS
        stair_pos.dark_sprite = S_DSTAIRS
        stair_pos.name = "stairs"
        stair_pos.sheet = S_TELEPORTER
        stair_pos.cols = 32
        stair_pos.rows = 32
        # Spawn stairs next to player for testing
        self.tiles[self.first_room[0]][self.first_room[1]].sprite = S_STAIRS
        self.tiles[self.first_room[0]][self.first_room[1]].name = "stairs"

    def create_room(self, room):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                test_room = pygame.Rect((room.x1, room.x2), (room.y1, room.y2))
                self.level[x][y].sprite = S_FLOOR
                self.level[x][y].block_path = False
                self.level[x][y].block_sight = False
                self.level[x][y].dark_sprite = S_DFLOOR
                if not self.first_room:
                    self.first_room = room.center()
                # Calculate corners and wall sides to place floor tiles

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