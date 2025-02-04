# Project Zomboid Map Parser

A Python library for parsing and analyzing map data from the game Project Zomboid. This library provides tools to read, process, and search through the game's map files, allowing you to explore and extract information about the game world.

## Features

- Parse Project Zomboid's binary map formats (`.lotpack` and `.lotheader` files)
- Convert between different coordinate systems (World, Cell, and Chunk coordinates)
- Search for specific tiles across the game world
- Process map data in parallel for improved performance
- Extract information about map cells, rooms, and tile placements
- Support for all map layers (floor, wall, and object tiles)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pz_map_parser.git
cd pz_map_parser
```

## Quick Start

Here's a simple example that demonstrates how to use the parser to search for specific tiles in the game world:

```python
from pathlib import Path
from zomboid_map_parser import Parser

# Initialize the parser with your game directory
parser = Parser(Path("C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media"))

# Parse all map data
parser.parse_all()
```

## Understanding Coordinate Systems

The parser handles three main coordinate systems used by Project Zomboid:

1. **World Coordinates** (`WorldCoord`)
   - Absolute position in tiles from the world origin (0,0)
   - Most precise coordinate system
   - Used for exact tile locations

2. **Cell Coordinates** (`CellCoord`)
   - Divides the world into 300x300 tile sections
   - Used by `.lotpack` and `.lotheader` files
   - Cell (0,0) contains world coordinates (0-299, 0-299)

3. **Chunk Coordinates** (`ChunkCoord`)
   - Divides cells into 10x10 tile sections
   - Used for efficient memory management
   - Each cell contains 30x30 chunks

The library provides utilities to convert between these coordinate systems:

```python
from zomboid_map_parser.utils import CoordinateConverter
from zomboid_map_parser.models.coordinates.absolute import WorldCoord

# Convert world coordinates to cell coordinates
world_pos = WorldCoord(x=750, y=450, z=0)
cell_coord, local_pos = CoordinateConverter.world_to_cell(world_pos)
```

## File Format Support

The parser supports the following Project Zomboid file formats:

- **`.lotpack`**: Contains map cell data including tile placements and room definitions
- **`.lotheader`**: Contains tile name mappings used by `.lotpack` files
- **`.tiles`**: Contains tile definitions and properties **(WIP)**

## Advanced Usage

### Parallel Processing

The parser supports parallel processing for improved performance when searching large areas:

```python
# Enable parallel processing with 4 worker threads
parser = Parser(game_dir, max_workers=4)

# Search tiles in parallel
results = parser.search_tiles(tile_names, parallel=True)
```

### Limiting Search Area

You can limit searches to specific regions using `BoundsCoord`:

```python
from zomboid_map_parser.utils import BoundsCoord

# Search only cells within these bounds
bounds = BoundsCoord(min_x=10, max_x=20, min_y=10, max_y=20)
results = parser.search_tiles(tile_names, bounds=bounds)
```

### Processing Individual Cells

For more granular control, you can process individual map cells:

```python

from zomboid_map_parser.models.coordinates.relative import LocalCellCoord
from zomboid_map_parser.models.coordinates.absolute import CellCoord

# Get a specific cell
cell_coord = CellCoord(x=10, y=10)
cell = parser.get_cell_at_coordinates(cell_coord)

if cell:
   # Access cell data
   for z in range(8):  # 8 height levels
      for x in range(300):
         for y in range(300):
            square = cell.data.get_square(LocalCellCoord(x, y, z))
            # Process tile data
            for tile in square.floor_tiles:
               print(f"Floor tile: {tile.texture_name}")
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to The Indie Stone for creating Project Zomboid
- Inspired by [BlindCoder's pz-mapmap command line](https://github.com/blind-coder/pz-mapmap)