import tcod as tcod

screen_width = 80
screen_height = 50
map_width = 80
map_height = 45
colors = {
    'dark_wall': tcod.Color(0, 0, 100),
    'dark_ground': tcod.Color(50, 50, 150)
}
player_x = int(screen_width / 2)
player_y = int(screen_height / 2)
