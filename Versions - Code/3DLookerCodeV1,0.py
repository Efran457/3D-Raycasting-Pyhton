import curses
import time
import math
import random

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

# Draw line function (only Diagonal Lines)
def draw_line(stdscr, y1, x1, y2, x2, char):
    max_y, max_x = stdscr.getmaxyx()
    
    # Clamp coordinates to screen bounds
    y1 = max(0, min(y1, max_y - 1))
    x1 = max(0, min(x1, max_x - 1))
    y2 = max(0, min(y2, max_y - 1))
    x2 = max(0, min(x2, max_x - 1))
    
    move = [0, 0]
    if y1 > y2:
        move[0] = -1
    elif y2 > y1:
        move[0] = 1
    if x1 > x2:  # x1 is right of x2
        move[1] = -1
    elif x2 > x1:
        move[1] = 1
    
    # Draw the line
    distance = max(abs(x2 - x1), abs(y2 - y1))
    for i in range(distance + 1):
        y = y1 + i * move[0]
        x = x1 + i * move[1]
        
        # Bounds checking and avoid bottom-right corner
        if 0 <= y < max_y and 0 <= x < max_x:
            if not (y == max_y - 1 and x == max_x - 1):
                try:
                    stdscr.addstr(y, x, char)
                except curses.error:
                    pass

# Draw rectangle function
def draw_rect(stdscr, point1, point2, point3, point4, char="#"):
    draw_line(stdscr, point1[0], point1[1], point2[0], point2[1], char)
    draw_line(stdscr, point2[0], point2[1], point3[0], point3[1], char)
    draw_line(stdscr, point3[0], point3[1], point4[0], point4[1], char)
    draw_line(stdscr, point4[0], point4[1], point1[0], point1[1], char)

# Fill rectangle function
def fill_rect(stdscr, y1, x1, y2, x2, char):
    max_y, max_x = stdscr.getmaxyx()
    start_y = max(0, min(y1, y2))
    end_y = min(max_y - 1, max(y1, y2))
    start_x = max(0, min(x1, x2))
    end_x = min(max_x - 1, max(x1, x2))
    
    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
            if not (y == max_y - 1 and x == max_x - 1):
                try:
                    stdscr.addstr(y, x, char)
                except curses.error:
                    pass

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
                        else:
                            char = " "
                        
                        try:
                            stdscr.addstr(screen_y, screen_x, char)
                        except curses.error:
                            pass
    
    # Draw player position and direction
    player_screen_y = offset_y + int(player.y * scale)
    player_screen_x = offset_x + int(player.x * scale)
    
    if player_screen_y < max_y and player_screen_x < max_x:
        try:
            stdscr.addstr(player_screen_y, player_screen_x, "@", curses.A_BOLD)
        except curses.error:
            pass
    
    # Draw direction indicator
    dir_length = 2
    dir_end_y = player_screen_y + int(player.dir_y * dir_length * scale)
    dir_end_x = player_screen_x + int(player.dir_x * dir_length * scale)
    
    if 0 <= dir_end_y < max_y and 0 <= dir_end_x < max_x:
        try:
            stdscr.addstr(dir_end_y, dir_end_x, "*")
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
                    stdscr.addstr(screen_y, screen_x, "▓")
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
    
    def rotate(self, delta_angle):
        self.angle += delta_angle
        self.dir_x = math.cos(self.angle)
        self.dir_y = math.sin(self.angle)
    
    def move_forward(self, game_map):
        new_x = self.x + self.dir_x * 0.3
        new_y = self.y + self.dir_y * 0.3
        if 0 <= int(new_y) < len(game_map) and 0 <= int(new_x) < len(game_map[0]):
            if game_map[int(new_y)][int(new_x)] == 0:
                self.x = new_x
                self.y = new_y
    
    def move_backward(self, game_map):
        new_x = self.x - self.dir_x * 0.3
        new_y = self.y - self.dir_y * 0.3
        if 0 <= int(new_y) < len(game_map) and 0 <= int(new_x) < len(game_map[0]):
            if game_map[int(new_y)][int(new_x)] == 0:
                self.x = new_x
                self.y = new_y

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
    RUNTIME = 0
    
    # Main loop
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP or key == ord('w'):
            player.move_forward(game_map)
        elif key == curses.KEY_DOWN or key == ord('s'):
            player.move_backward(game_map)
        elif key == curses.KEY_LEFT or key == ord('a'):
            player.rotate(-0.1)
        elif key == curses.KEY_RIGHT or key == ord('d'):
            player.rotate(0.1)
        elif key == ord('m'):
            show_minimap = not show_minimap
        elif key == ord('r'):
            # Regenerate maze
            game_map = generate_maze(maze_width, maze_height)
            player = Player([1, 1], [1, 0])
        
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
            ceiling_end = max(0, (max_y - wall_height) // 2)
            wall_start = ceiling_end
            wall_end = min(max_y - 1, wall_start + wall_height)
            
            # Choose shading based on distance
            if distance < 2:
                char = "#"
            elif distance < 4:
                char = "+"
            elif distance < 8:
                char = "-"
            elif distance < 12:
                char = "."
            else:
                char = " "
            
            # Draw the column
            # Ceiling
            for y in range(0, ceiling_end):
                try:
                    stdscr.addstr(y, i, " ")
                except curses.error:
                    pass
            
            # Wall
            for y in range(wall_start, wall_end):
                try:
                    stdscr.addstr(y, i, char)
                except curses.error:
                    pass
            
            # Floor
            for y in range(wall_end, max_y):
                try:
                    stdscr.addstr(y, i, " ")
                except curses.error:
                    pass
        
        # Display controls
        try:
            stdscr.addstr(0, 0, "W/S: Move | A/D: Rotate | M: Map | R: Restart | Q: Quit", curses.A_REVERSE)
        except curses.error:
            pass
        
        # Draw minimap
        if show_minimap:
            minimap_scale = 1
            minimap_offset_y = 2
            minimap_offset_x = 2
            draw_minimap(stdscr, game_map, player, minimap_offset_y, minimap_offset_x, minimap_scale)
        
        RUNTIME += 0.1
        stdscr.refresh()
    
    RUNTIME = round(RUNTIME, 10)
    print("Thanks for playing!")
    print(f"Runtime = {RUNTIME}")
    time.sleep(10)

curses.wrapper(main)