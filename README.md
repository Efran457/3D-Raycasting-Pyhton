# 3D-Raycasting-Pyhton
This is a 3D Racasting programm that uses a python library called curses (curses makes it easy to display text on a corandiant)

# 3D Looker

A terminal-based 3D maze explorer using ASCII raycasting rendering. Navigate through procedurally generated labyrinths in your command line!

![3D Looker Demo](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)

## Features

- **Raycasting 3D Renderer** - Classic pseudo-3D rendering similar to Wolfenstein 3D
- **Procedural Maze Generation** - Uses recursive backtracking algorithm to create perfect mazes
- **Real-time Navigation** - Smooth WASD/Arrow key controls
- **Interactive Minimap** - Toggle-able overhead view showing your position and direction
- **Distance-based Shading** - Walls appear darker when closer, creating depth perception
- **Regenerate Mazes** - Press R to explore a brand new randomly generated labyrinth

## Screenshots

```
W/S: Move | A/D: Rotate | M: Map | R: New Maze | Q: Quit
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓█ █ █████ █████ █ █▓
▓  @ █   █ █   █ █  ▓
▓█ █ █ █ █ █ █ █ █ █▓
▓█ █   █ █   █   █ █▓
▓█ █████ █████████ █▓
▓█ █   █ █       █ █▓
▓█ █ █ █ █ █████ █ █▓
▓█   █   █ █   █   █▓
▓█████████ █ █ █████▓
▓█       █   █     █▓
▓█ █████ █████████ █▓
▓█ █   █         █ █▓
▓█ █ █ █████████ █ █▓
▓█   █           █  ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

             ##########
            ############
           ##############
          ################
         ##################
        ####################
       ######################
      ########################
     ##########################
    ############################
   ##############################
  ################################
```

## Installation

### Prerequisites

- Python 3.x
- Terminal with Unicode support (most modern terminals)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/3d-looker.git
cd 3d-looker
```

2. Run the game:
```bash
python 3DLooker.py
```

No additional dependencies required - uses Python's built-in `curses` library!

## Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move forward |
| `S` / `↓` | Move backward |
| `A` / `←` | Rotate left |
| `D` / `→` | Rotate right |
| `M` | Toggle minimap |
| `R` | Regenerate new maze |
| `Q` | Quit game |

## How It Works

### Raycasting Algorithm

The renderer uses a raycasting technique where:
1. For each column of the screen, a ray is cast from the player's position
2. The ray travels until it hits a wall
3. Wall height is calculated based on distance (closer = taller)
4. Fish-eye distortion is corrected using cosine compensation
5. Distance-based shading creates depth perception

### Maze Generation

Mazes are generated using the **recursive backtracking algorithm**:
1. Start with a grid filled with walls
2. Choose a random starting cell and mark it as a passage
3. While there are unvisited neighbors:
   - Choose a random unvisited neighbor
   - Remove the wall between them
   - Move to the neighbor and repeat
4. Backtrack when stuck until all cells are visited

This creates a "perfect maze" - exactly one path between any two points.

## Customization

### Adjust Maze Size

Edit the `main()` function:
```python
maze_width = 21   # Must be odd number
maze_height = 15  # Must be odd number
```

### Change Field of View

```python
fov = math.pi / 3  # 60 degrees (π/3 radians)
```

### Modify Movement Speed

In the `Player` class:
```python
def move_forward(self, game_map):
    new_x = self.x + self.dir_x * 0.3  # Change 0.3 to adjust speed
```

### Customize Shading

In the raycasting loop:
```python
if distance < 2:
    char = "#"
elif distance < 4:
    char = "+"
elif distance < 8:
    char = "-"
# Add more levels or change characters
```

## Technical Details

- **Language**: Python 3
- **Rendering**: ASCII characters using curses library
- **Rendering Method**: Column-based raycasting
- **Frame Rate**: ~60 FPS (16ms timeout)
- **Collision Detection**: Grid-based boundary checking
- **Map Representation**: 2D array (1 = wall, 0 = passage)

## Troubleshooting

### Windows Issues

If you encounter problems on Windows:
1. Install Windows Terminal for better Unicode support
2. Or use WSL (Windows Subsystem for Linux)
3. Alternative: Try `windows-curses` package:
```bash
pip install windows-curses
```

### Terminal Size

If the display looks broken, resize your terminal to at least 80x24 characters.

### Performance Issues

- Reduce `num_rays` for faster rendering
- Decrease maze size
- Increase `stdscr.timeout()` value

## Future Enhancements

- [ ] Textured walls with different characters/colors
- [ ] Multiple floor levels
- [ ] Enemies/collectibles
- [ ] Save/load maze feature
- [ ] Different maze generation algorithms
- [ ] Sound effects (terminal beep)
- [ ] Multiplayer support

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic games like Wolfenstein 3D and Doom
- Raycasting technique based on Lode Vandevenne's raycasting tutorial
- Maze generation using classic recursive backtracking algorithm

## Author

Created with ❤️ by [Your Name]

---

**Enjoy exploring the mazes! 🎮**
