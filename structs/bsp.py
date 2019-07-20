def generate_bsp_level(self):
    tiles = [[StrucTile(False, False) for y in range(self.height)] for x in range(self.width)]
    bsp_rooms = []

    # New root node
    bsp = tcod.bsp_new_with_size(0, 0, GRIDWIDTH, GRIDHEIGHT)

    # Split into nodes
    tcod.bsp_split_recursive(bsp, 0, DEPTH, MIN_SIZE + 1, MIN_SIZE + 1, 1, 1)
    # Traverse the nodes and create rooms
    tcod.bsp_traverse_inverted_level_order(bsp, self.traverse_node)

    stairs_location = random.choice(bsp_rooms)
    bsp_rooms.remove(stairs_location)
    # stairs = StrucTile(False, False, S_ENEMY)

    player_room = random.choice(bsp_rooms)
    bsp_rooms.remove(player_room)

    for room in bsp_rooms:
        new_room = pygame.Rect(room[0], room[1], 2, 2)

    return 0


def traverse_node(self, node, dat, bsp_rooms):
    if tcod.bsp_is_leaf(node):
        min_x = node.x + 1
        max_x = node.x + node.w - 1
        min_y = node.y + 1
        max_y = node.y + node.h - 1

        if max_x == GRIDWIDTH - 1:
            max_x -= 1
        if max_y == GRIDHEIGHT - 1:
            max_y -= 1

        if FULL_ROOMS == False:
            min_x = tcod.random_get_int(None, min_x, max_x - MIN_SIZE + 1)
            min_y = tcod.random_get_int(None, min_y, max_y - MIN_SIZE + 1)
            max_x = tcod.random_get_int(None, min_x + MIN_SIZE - 2, max_x)
            max_y = tcod.random_get_int(None, min_y, + MIN_SIZE - 2, max_y)

        node.x = min_x
        node.y = min_y
        node.w = max_x - min_x + 1
        node.h = max_y - min_y + 1

        # Dig room
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                self.tiles[x][y].block_path = False
                self.tiles[x][y].block_sight = False

        bsp_rooms.append(((min_x + max_x) / 2, (min_y + max_y) / 2))
    else:
        left = tcod.bsp_left(node)
        right = tcod.bsp_right(node)
        node.x = min(left.x, right.x)
        node.y = min(left.y, right.y)
        node.w = max(left.x + left.w, right.x + right.w) - node.x
        node.h = max(left.y + left.h, right.y + right.h) - node.y
        if node.horizontal:
            if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                x1 = tcod.random_get_int(None, left.x, left.x + left.w - 1)
                x2 = tcod.random_get_int(None, right.x, right.x + right.w - 1)
                y = tcod.random_get_int(None, left.y + left.h, right.y)
                self.vline_up(x1, y - 1)
                self.hline(x1, y, x2)
                self.vline_down(x2, y + 1)

            else:
                minx = max(left.x, right.x)
                maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                x = tcod.random_get_int(None, minx, maxx)

                # catch out-of-bounds attempts
                while x > MAP_WIDTH - 1:
                    x -= 1

                self.vline_down(x, right.y)
                self.vline_up(x, right.y - 1)
        else:
            if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                y1 = tcod.random_get_int(None, left.y, left.y + left.h - 1)
                y2 = tcod.random_get_int(None, right.y, right.y + right.h - 1)
                x = tcod.random_get_int(None, left.x + left.w, right.x)
                self.hline_left(x - 1, y1)
                self.vline(x, y1, y2)
                self.hline_right(x + 1, y2)
            else:
                miny = max(left.y, right.y)
                maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                y = tcod.random_get_int(None, miny, maxy)

                # catch out-of-bounds attempts
                while y > MAP_HEIGHT - 1:
                    y -= 1

                self.hline_left(right.x - 1, y)
                self.hline_right(right.x, y)
    return True


def vline(self, x, y1, y2):
    if y1 > y2:
        y1, y2 = y2, y1

    for y in range(y1, y2 + 1):
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False


def vline_up(self, x, y):
    while y >= 0 and self.tiles[x][y].blocked:
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False
        y -= 1


def vline_down(self, x, y):
    while y < MAP_HEIGHT and self.tiles[x][y].blocked:
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False
        y += 1


def hline(self, x1, y, x2):
    if x1 > x2:
        x1, x2 = x2, x1
    for x in range(x1, x2 + 1):
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False


def hline_left(self, x, y):
    while x >= 0 and self.tiles[x][y].blocked:
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False
        x -= 1


def hline_right(self, x, y):
    while x < MAP_WIDTH and self.tiles[x][y].blocked:
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False
        x += 1