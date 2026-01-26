import curses
import time
import math
import random
import curses

# Setup colors
def rgb(r, g, b):
    #Convert 0-255 RGB to curses 0-1000
    return int(r / 255 * 1000), int(g / 255 * 1000), int(b / 255 * 1000)

def darken_color(r, g, b, factor):
    #Darken RGB color by factor (0.0=black, 1.0=original)
    r_new = int(r * factor)
    g_new = int(g * factor)
    b_new = int(b * factor)
    return r_new, g_new, b_new

def set_color_pair(pair_id, color_id, r, g, b, bg=-1):
    if curses.can_change_color():
        curses.init_color(color_id, *rgb(r, g, b))
    curses.init_pair(pair_id, color_id, bg)

# Setup colors with shading
def init_pair_colors(base_rgb, factors):
    curses.start_color()
    curses.use_default_colors()

    for i, f in enumerate(factors):
        r_d, g_d, b_d = darken_color(*base_rgb, f)
        set_color_pair(i + 1, 20 + i, r_d, g_d, b_d)  # pair_id = i+1, color_id = 20+i

    # Always keep white for minimap/info
    set_color_pair(len(factors) + 1, 30, 255, 255, 255)

def init_colors(WallColor, GroundColor, SkyColor):
    # Example: factors for distance shading
    init_pair_colors(WallColor, [0.9, 0.8, 0.65, 0.5, 0.3, 0.0])
    # Background color for floor
    set_color_pair(50, 50, GroundColor[0], GroundColor[1], GroundColor[2])
    set_color_pair(51, 51, SkyColor[0], SkyColor[1], SkyColor[2])


def CheckTime(runtime, daycolor):
    cycle = runtime % 60
    t = abs(30 - cycle) / 30  # 0 → 1 → 0
    return list(darken_color(*daycolor, 0.3 + 0.7 * t))

# Generate a proper maze using recursive backtracking
def generate_maze(width, height):
    # Create a grid filled with walls (1)
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Starting position (must be odd coordinates)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    
    # Stack for backtracking
    stack = [(start_x, start_y)]
    
    # Directions: right, down, left, up
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    
    while stack:
        x, y = stack[-1]
        
        # Find unvisited neighbors
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
                neighbors.append((nx, ny, dx, dy))
        
        if neighbors:
            # Choose random neighbor
            nx, ny, dx, dy = random.choice(neighbors)
            
            # Remove wall between current cell and chosen neighbor
            maze[y + dy // 2][x + dx // 2] = 0
            maze[ny][nx] = 0
            
            stack.append((nx, ny))
        else:
            # Backtrack
            stack.pop()
    
    return maze

# Draw minimap
def draw_minimap(stdscr, game_map, player, offset_y, offset_x, scale=2):
    max_y, max_x = stdscr.getmaxyx()
    
    # Draw map border
    map_height = len(game_map) * scale
    map_width = len(game_map[0]) * scale
    
    # Draw the map tiles
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            for dy in range(scale):
                for dx in range(scale):
                    screen_y = offset_y + y * scale + dy
                    screen_x = offset_x + x * scale + dx
                    
                    if screen_y < max_y and screen_x < max_x:
                        if game_map[y][x] == 1:
                            char = "█"
                            color = curses.color_pair(7)
                        else:
                            char = " "
                            color = curses.color_pair(7)
                        
                        try:
                            stdscr.addstr(screen_y, screen_x, char, color)
                        except curses.error:
                            pass
    
    # Draw player position and direction
    player_screen_y = offset_y + int(player.y * scale)
    player_screen_x = offset_x + int(player.x * scale)
    
    if player_screen_y < max_y and player_screen_x < max_x:
        try:
            stdscr.addstr(player_screen_y, player_screen_x, "O", curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass
    
    # Draw direction indicator
    dir_length = 2
    dir_end_y = player_screen_y + int(player.dir_y * dir_length * scale)
    dir_end_x = player_screen_x + int(player.dir_x * dir_length * scale)
    
    if 0 <= dir_end_y < max_y and 0 <= dir_end_x < max_x:
        try:
            # Convert screen coordinates back to map coordinates
            map_y = (dir_end_y - offset_y) // scale
            map_x = (dir_end_x - offset_x) // scale
        
            # Check bounds and wall status
            if 0 <= map_y < len(game_map) and 0 <= map_x < len(game_map[0]):
                if game_map[map_y][map_x] == 1:
                    stdscr.addstr(dir_end_y, dir_end_x, "*", curses.A_REVERSE)
                else:   
                    stdscr.addstr(dir_end_y, dir_end_x, "*", curses.color_pair(7))
            else:
                stdscr.addstr(dir_end_y, dir_end_x, "*", curses.color_pair(7))
        except curses.error:
            pass
    
    # Draw border around minimap
    for y in range(map_height + 2):
        for x in range(map_width + 2):
            screen_y = offset_y - 1 + y
            screen_x = offset_x - 1 + x
            
            if screen_y >= max_y or screen_x >= max_x:
                continue
            
            if y == 0 or y == map_height + 1 or x == 0 or x == map_width + 1:
                try:
                    stdscr.addstr(screen_y, screen_x, "▓", curses.color_pair(4))
                except curses.error:
                    pass

def DrawInfo(stdscr, y, x, msgs):
    try:
        for i in range(len(msgs)):
            stdscr.addstr(y+i, x, msgs[i], curses.A_REVERSE)
    except curses.error:
        pass

# Player class
class Player:
    def __init__(self, pos, direction):
        self.x = pos[1]
        self.y = pos[0]
        self.dir_x = direction[1]
        self.dir_y = direction[0]
        self.angle = math.atan2(direction[0], direction[1])
        self.pitch = 0   # look up / down

    def rotate(self, delta_angle):
        self.angle += delta_angle
        self.dir_x = math.cos(self.angle)
        self.dir_y = math.sin(self.angle)

    def move_forward(self, game_map):
        new_x = self.x + self.dir_x * 0.3
        new_y = self.y + self.dir_y * 0.3
        if game_map[int(new_y)][int(new_x)] == 0:
            self.x, self.y = new_x, new_y

    def move_backward(self, game_map):
        new_x = self.x - self.dir_x * 0.3
        new_y = self.y - self.dir_y * 0.3
        if game_map[int(new_y)][int(new_x)] == 0:
            self.x, self.y = new_x, new_y

    def move_left(self, game_map):
        nx = self.x + self.dir_y * 0.1
        ny = self.y - self.dir_x * 0.1
        if game_map[int(ny)][int(nx)] == 0:
            self.x, self.y = nx, ny

    def move_right(self, game_map):
        nx = self.x - self.dir_y * 0.1
        ny = self.y + self.dir_x * 0.1
        if game_map[int(ny)][int(nx)] == 0:
            self.x, self.y = nx, ny


# Raycasting function
def cast_ray(player, game_map, angle):
    ray_x = player.x
    ray_y = player.y
    ray_dir_x = math.cos(angle)
    ray_dir_y = math.sin(angle)
    
    max_distance = 20
    step = 0.1
    distance = 0
    
    while distance < max_distance:
        ray_x += ray_dir_x * step
        ray_y += ray_dir_y * step
        distance += step
        
        map_x = int(ray_x)
        map_y = int(ray_y)
        
        if map_x < 0 or map_x >= len(game_map[0]) or map_y < 0 or map_y >= len(game_map):
            return max_distance
        
        if game_map[map_y][map_x] == 1:
            return distance
    
    return max_distance

# Main function to run the 3D looker
def main(stdscr):
    # Setup Curses
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(16)  # ~60 FPS
    stdscr.keypad(True)
    
    # Initialize colors (Darker Color Recomanded)
    WallColor = [0, 230, 203]  # wall color
    GroundColor = [3, 252, 132]      # background color
    dayColor = [135, 206, 235]        # day sky color]
    SkyColor = darken_color(dayColor[0],dayColor[1],dayColor[2], 0.5)        # sky color
    init_colors(WallColor, GroundColor, SkyColor)
    
    # Get maximum screen dimensions
    max_y, max_x = stdscr.getmaxyx()
    
    # Generate a proper maze (must have odd dimensions for the algorithm)
    maze_width = 21
    maze_height = 15
    game_map = generate_maze(maze_width, maze_height)
    
    # Player starts at a guaranteed open space
    player = Player([1, 1], [1, 0])
    
    fov = math.pi / 3  # 60 degrees field of view
    num_rays = max_x
    
    show_minimap = False
    show_Info = False
    RUNTIME = 0
    
    # Main loop
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('w'):
            player.move_forward(game_map)
        elif key == ord('s'):
            player.move_backward(game_map)
        elif key == ord('a'):
            player.move_left(game_map)
        elif key == ord('d'):
            player.move_right(game_map)
        elif key == curses.KEY_LEFT:
            player.rotate(-0.1)
        elif key == curses.KEY_RIGHT:
            player.rotate(0.1)
        elif key == curses.KEY_UP:
            player.pitch += 2     # look up
        elif key == curses.KEY_DOWN:
            player.pitch -= 2     # look down
        elif key == ord('m'):
            show_minimap = not show_minimap
        elif key == ord('r'):
            # Regenerate maze
            game_map = generate_maze(maze_width, maze_height)
            player = Player([1, 1], [1, 0])
        elif key == ord('i'):
            show_Info = not show_Info
        
        player.pitch = max(-max_y // 2, min(max_y // 2, player.pitch)) # Roatation

        stdscr.clear()
        
        # Raycasting
        for i in range(num_rays):
            ray_angle = player.angle - fov / 2 + (i / num_rays) * fov
            distance = cast_ray(player, game_map, ray_angle)
            
            # Fix fish-eye effect
            distance *= math.cos(ray_angle - player.angle)
            
            # Calculate wall height
            if distance > 0:
                wall_height = int((max_y / distance) * 2)
            else:
                wall_height = max_y
            
            # Draw ceiling, wall, and floor
            center_y = max_y // 2 + player.pitch

            wall_start = int(center_y - wall_height // 2)
            wall_end = int(center_y + wall_height // 2)

            wall_start = max(0, wall_start)
            wall_end = min(max_y - 1, wall_end)

            
            # Choose shading and COLOR based on distance - rainbow gradient!
            if distance < 1.5:
                char = "█"
                charColor = curses.color_pair(1)  # very near
            elif distance < 3:
                char = "▓"
                charColor = curses.color_pair(2)  # near
            elif distance < 5:
                char = "▒"
                charColor = curses.color_pair(3)  # medium
            elif distance < 7:
                char = "▒"
                charColor = curses.color_pair(4)  # far
            elif distance < 10:
                char = "░"
                charColor = curses.color_pair(5)  # very far
            elif distance < 14:
                char = "█"
                charColor = curses.color_pair(6)  # ultra far
            else:
                char = " "
                charColor = curses.color_pair(7)  # invisible

            
            # Draw the column
            # Ceiling
            for y in range(0, wall_start):
                try:
                    stdscr.addstr(y, i, "▓", curses.color_pair(51))
                except curses.error:
                    pass

            # Wall
            for y in range(wall_start, wall_end):
                try:
                    stdscr.addstr(y, i, char, charColor)
                except curses.error:
                    pass

            
            # Floor
            for y in range(wall_end, max_y):
                try:
                    stdscr.addstr(y, i, "▒", curses.color_pair(50))
                except curses.error:
                    pass
        
        # Display controls
        try:
            stdscr.addstr(0, 0, "W/S: Move | A/D: Rotate | [M]ap | [R]estart | [Q]uit | [I]nfo ", curses.A_REVERSE)
        except curses.error:
            stdscr.addstr(0, 0, "...", curses.A_REVERSE)

        # Check if night time is true
        newSky = CheckTime(RUNTIME, dayColor)

        # update sky color dynamically
        set_color_pair(51, 51, newSky[0], newSky[1], newSky[2])

        
        # Draw minimap
        if show_minimap:
            minimap_scale = 1
            minimap_offset_y = 2
            minimap_offset_x = 2
            draw_minimap(stdscr, game_map, player, minimap_offset_y, minimap_offset_x, minimap_scale)
        if show_Info:
            info_msgs = [
                f"Player Position: ({player.x:.2f}, {player.y:.2f})",
                f"Player Direction: ({player.dir_x:.2f}, {player.dir_y:.2f})",
                f"FPS: {int(1 / 0.016)}",
                f"Runtime: {RUNTIME:.1f} seconds ({minruntime} {"Minute" if minruntime == 1 else "Minutes"})",
                f"Map Size: {maze_width} x {maze_height}",
                f"Show Minimap: {'ON' if show_minimap else 'OFF'}",
                f"Main RBG Colors = Wall{WallColor},Ground{GroundColor},Sky{newSky}"
            ]
            infolengt = 0
            for msg in info_msgs:
                if len(msg) > infolengt:
                    infolengt = len(msg)

            DrawInfo(stdscr, 1, max_x - infolengt-1, info_msgs)
        RUNTIME += 0.1
        minruntime = int(round(RUNTIME, 10) // 60) # RUNTIME in Minutes
        stdscr.refresh()
    stdscr.clear()
    RUNTIME = round(RUNTIME, 10)
    minruntime = int(RUNTIME // 60) # RUNTIME in Minutes
    stdscr.addstr(0, 0, "Thanks for playing!", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(1, 0, f"Runtime = {RUNTIME} ({minruntime} {"Minute" if minruntime == 1 else "Minutes"})", curses.color_pair(2))
    stdscr.refresh()
    time.sleep(3)

curses.wrapper(main)
