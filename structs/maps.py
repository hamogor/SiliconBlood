#  __  __
# |  \/  | __ _ _ __
# | |\/| |/ _` | '_ \
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/
#              |_|

# libraries
import tcod as libtcod

# game files
import settings
import random
from structs.tile import StrucTile


class MapGeneration:

    ''' This is an object that represents the physical space of the game world'''

    def __init__(self, map_width, map_height):

        self.width = map_width
        self.height = map_height

        # initializes an empty map
        self.map_tiles = [[StrucTile(True, True) for y in range(0, self.height)]
                                                 for x in range(0, self.width)]

        # Map properties
        self.list_rooms = []
        self.listRegions = []
        self.listObjects = []

    def gen_map_random_rooms(self,
                            num_of_rooms,
                            room_min_width,
                            room_max_width,
                            room_min_height,
                            room_max_height):

        '''Creates the default map.'''

        for i in range(num_of_rooms):

            w = libtcod.random_get_int(0, room_max_width, room_min_width)
            h = libtcod.random_get_int(0, room_max_height, room_min_height)

            x = libtcod.random_get_int(0, 2, self.width - w - 2)
            y = libtcod.random_get_int(0, 2, self.height - h - 2)

            # Create the room
            new_room = obj_room((x, y), (w, h))

            failed = False

            # check for interference
            for other_room in self.list_rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # place room
                self.dig_room(new_room)
                current_center = new_room.center

                if len(self.list_rooms) != 0:

                    previous_center = self.list_rooms[-1].center

                    # dig tunnels
                    self.dig_tunnels(current_center, previous_center)

                self.list_rooms.append(new_room)

        self.assign_tiles()

        # create FOV_MAP
        make_fov(self.map_tiles)

        self.place_object_by_room()

    def genMapDrunkWalk(self):

        # (floor maker x, and y)
        floor_maker = (self.width // 2, self.height // 2)

        self.map_tiles[self.width // 2][self.height // 2].block_path = False

        globalvars.PLAYER.set_position(floor_maker)

        # choose the possible inputs that lead in certain directions
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

        currentDirection = globalvars.RANDOM_ENGINE.choice(directions)
        potential_x, potential_y = globalvars.RANDOM_ENGINE.choice(directions)

        for x in range(NUM_OF_STEPS):

            if libtcod.random_get_int(0, 0, 100) < (CHANCE_OF_DIRECTION_CHANGE * 100):
                potential_x, potential_y = globalvars.RANDOM_ENGINE.choice(directions)

            floor_x, floor_y = floor_maker
            floor_x += potential_x
            floor_y += potential_y

            viable = ( floor_x< MAP_WIDTH - 1 and
                       floor_x > 0 and
                       floor_y < MAP_HEIGHT - 1 and
                       floor_y > 0)

            while not viable:

                potential_x, potential_y = globalvars.RANDOM_ENGINE.choice(directions)

                floor_x, floor_y = floor_maker
                floor_x += potential_x
                floor_y += potential_y

                viable = ( floor_x< MAP_WIDTH - 1 and
                           floor_x > 0 and
                           floor_y < MAP_HEIGHT - 1 and
                           floor_y > 0)

                # end of WHILE loop

            self.map_tiles[floor_x][floor_y].block_path = False

            floor_maker = (floor_x, floor_y)

            # End of FOR LOOP

        self.assign_tiles()

        # create FOV_MAP
        make_fov(self.map_tiles)

    def genMapBinarySpace(self):

        #############
        ## STEP 00 ##
        #############
        ## PREPARATION ##
        self.listRegions = [ [obj_room((0, 0), (MAP_WIDTH, MAP_HEIGHT))] ]

        #############
        ## STEP 01 ##
        #############
        ## DIVIDE SPACE ##
        for i in range(0, BSP_TIMES_SPLIT):

            tempList = []

            # iterate through list and split each region
            for region in self.listRegions[-1]:

                # choose split size
                splitPct = random.uniform(BSP_MIN_SPLIT, BSP_MAX_SPLIT)

                # If the split number is odds, split vertically
                if ( (i % 2) != 0 ):

                    splitValue = int(region.w * splitPct)

                    region01 = obj_room( (region.x1, region.y1),
                                         (splitValue, region.h) )

                    region02 = obj_room( (region01.x1 + region01.w, region.y1),
                                         (region.w - splitValue, region.h) )

                else: #otherwise split the rooms horizontally

                    splitValue = int(region.h * splitPct)

                    region01 = obj_room( (region.x1, region.y1),
                                          (region.w, splitValue) )

                    region02 = obj_room( (region.x1, region01.y1 + region01.h),
                                          (region.w, region.h - splitValue) )

                tempList.append(region01)
                tempList.append(region02)

            ###### END OF FOR LOOP ######
            # add the new group of regions to the master list
            self.listRegions.append(tempList)

        #############
        ## STEP 02 ##
        #############
        ## FINISH THE 'TREE' OR 'REGIONS' ##

        # loop through and fill out complete groups
        for levelNumber, regionsInLevel in enumerate(self.listRegions):
            currentNumOfRegionsInGroup = len(regionsInLevel)
            neededNumOfRegionsInGroup = len(self.listRegions[-1]) / currentNumOfRegionsInGroup

            tempList = []

            for listNumber in range(currentNumOfRegionsInGroup):
                listStart = listNumber * neededNumOfRegionsInGroup
                listEnd = listStart + neededNumOfRegionsInGroup
                tempList.append(self.listRegions[-1][listStart:listEnd])

            self.listRegions[levelNumber] = tempList

        #delete the useless last level
        del self.listRegions[-1]

        #############
        ## STEP 03 ##
        #############
        ## ROOM CREATION ##
        for region in self.listRegions[0][0]:
            newRoom = obj_room((region.x1 + 1, region.y1 + 1),
                               (region.w - 2, region.h - 2))

            self.dig_room(newRoom)
            self.list_rooms.append(newRoom)

        #############
        ## STEP 04 ##
        #############
        ## CONNECT ROOMS ##
        for i, groupRegions in enumerate(reversed(self.listRegions)):
            numOfGroups = len(groupRegions)
            numOfItems = len(groupRegions[0])

            if numOfItems == 2:
                for pair in groupRegions:
                    self.dig_tunnels(pair[0].center, pair[1].center)

            if numOfItems < (2 ** BSP_TIMES_SPLIT):
                for x in range(numOfGroups / 2):
                    setListBegin = x * 2
                    setListEnd = setListBegin + 2

                    roomChoice1 = globalvars.RANDOM_ENGINE.choice(groupRegions[setListBegin:setListEnd][0])
                    roomChoice2 = globalvars.RANDOM_ENGINE.choice(groupRegions[setListBegin:setListEnd][1])

                    self.dig_tunnels(roomChoice1.center, roomChoice2.center)

        #############
        ## STEP 05 ##
        #############
        ## PLACE OBJECTS ##
        globalvars.PLAYER.set_position(self.list_rooms[0].center)

        ## TODO add objects

        #############
        ## STEP 06 ##
        #############
        ## FINISHING TOUCHES ##
        # autotiling assignments
        self.assign_tiles()

        # create FOV_MAP
        make_fov(self.map_tiles)

    def dig_room(self, new_room):
        for x in range(new_room.x1, new_room.x2):
            for y in range(new_room.y1, new_room.y2):
                try:
                    self.map_tiles[x][y].block_path = False
                except:
                    print((x, y))

    def dig_tunnels(self, coords1, coords2):

        coin_flip = (libtcod.random_get_int(0, 0, 1) == 1)

        x1, y1 = coords1
        x2, y2 = coords2

        if coin_flip:

            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map_tiles[x][y1].block_path = False

            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map_tiles[x2][y].block_path = False

        else:

            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map_tiles[x1][y].block_path = False

            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map_tiles[x][y2].block_path = False

    def place_object_by_room(self):

        if self.list_rooms:

            current_level = len(globalvars.GAME.maps_previous) + 1

            top_level = (current_level == 1)
            final_level = (current_level == MAP_NUM_LEVELS)

            for room in self.list_rooms:

                first_room = (room == self.list_rooms[0])
                last_room = (room == self.list_rooms[-1])

                if first_room: globalvars.PLAYER.set_position(room.center)

                if first_room and top_level:
                    generator.portal(room.center)

                if first_room and not top_level:
                    generator.stairs((globalvars.PLAYER.x, globalvars.PLAYER.y), downwards = False)

                if last_room:
                    if final_level:
                        generator.LAMP(room.center)
                    else:
                        generator.stairs(room.center)

                x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

                generator.enemy((x, y))

                x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

                generator.item((x, y))

    def assign_tiles(self):
        #loop through map looking for the walls, then assign bitoperator
        for x in range(len(self.map_tiles)):
            for y in range(len(self.map_tiles[0])):

                # check tile for wall status
                tile_is_wall = self.checkForWall(x, y)

                if tile_is_wall:
                    # create tile var
                    tile_assignment = 0
                    # add bitmask value
                    if self.checkForWall(x, y-1): tile_assignment += 1
                    if self.checkForWall(x+1, y): tile_assignment += 2
                    if self.checkForWall(x, y+1): tile_assignment += 4
                    if self.checkForWall(x-1, y): tile_assignment += 8

                    self.map_tiles[x][y].assignment = tile_assignment

    def checkForObjects(self, coords_x, coords_y):

        '''Get a list of every object at a coordinate.

        Args:
            coords_x (int): x axis map coordinate of current map to check
            coords_y (int): y axis map coordinate of current map to check

        Returns:
            object_options (list): list of every object at the coordinate.

        '''

        object_options = [obj for obj in self.listObjects
                          if obj.x == coords_x and obj.y == coords_y]

        return object_options

    def checkForWall(self, x, y):

        if (x < 0 or
            y < 0 or
            x >= MAP_WIDTH or
            y >= MAP_HEIGHT):
            return False

        else: return self.map_tiles[x][y].block_path

    def checkForCreature(self, x, y, exclude_object = None):

        '''Check the current map for creatures at specified location.

        This function looks at that location for any object that has a creature
        component and returns it.  Optional argument allows user to exclude an
        object from the search, usually the Player

        Args:
            x (int): x map coord to check for creature
            y (int): y map coord to check for creature
            exclude_object(obj_Actor, optional): if an object is passed into this
                function, this object will be ignored by the search.

        Returns:
            target (obj_Actor): but only if found at the location specified in the
                arguments and if not excluded.

        '''

        # initialize target var to None type
        target = None

        # optionally exclude an object
        if exclude_object:

            # check objectlist to find creature at that location that isn't excluded
            for object in self.listObjects:
                if (object is not exclude_object and
                    object.x == x and
                    object.y == y and
                    object.creature):

                    # if object is found, set target var to object
                    target = object

                if target:
                    return target

        else:
        # check objectlist to find any creature at that location
            for object in self.listObjects:
                if (object.x == x and
                    object.y == y and
                    object.creature):

                    target = object

                if target:
                    return target

class obj_room:

    ''' This is a rectangle that lives on the map '''

    def __init__(self, coords, size):

        self.x1, self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2

        return (center_x, center_y)

    def intersect(self, other):

        # return True if other obj intersects with this one
        objects_intersect = (self.x1 <= other.x2 and self.x2 >= other.x1 and
                             self.y1 <= other.y2 and self.y2 >= other.y1)

        return objects_intersect

def make_fov(incoming_map):

    '''Creates an FOV map based on a map.

    Args:
        incoming_map (array): map, usually created with create

    Effects:
        generates the FOV_MAP

    '''

    globalvars.FOV_MAP = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(globalvars.FOV_MAP, x, y,
                not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def calculate_fov():

    '''Calculates the FOV based on the Player's perspective.

    Accesses the global variable FOV_CALCULATE, if FOV_CALCULATE is True, sets
    it to False and recalculates the FOV.

    '''

    if globalvars.FOV_CALCULATE:

        # reset FOV_CALCULATE
        globalvars.FOV_CALCULATE = False

        # run the calculation function
        libtcod.map_compute_fov(globalvars.FOV_MAP, globalvars.PLAYER.x,
                                globalvars.PLAYER.y,
                                TORCH_RADIUS,
                                FOV_LIGHT_WALLS,
                                FOV_ALGO)

def find_line(coords1, coords2):
    ''' Converts two x, y coords into a list of tiles.

    coords1 : (x1, y1)
    coords2 : (x2, y2)
    '''
    x1, y1 = coords1

    x2, y2 = coords2

    libtcod.line_init(x1, y1, x2, y2)

    calc_x, calc_y = libtcod.line_step()

    coord_list = []

    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    while (not calc_x is None):

        coord_list.append((calc_x, calc_y))

        calc_x, calc_y = libtcod.line_step()

    return coord_list

def find_radius(coords, radius):

    center_x, center_y = coords

    tile_list = []

    start_x = (center_x - radius)
    end_x = (center_x + radius + 1)

    start_y = (center_y - radius)
    end_y = (center_y + radius + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            tile_list.append((x, y))

    return tile_list
