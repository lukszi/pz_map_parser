# File Types

MapMap reads several different types of files:

1. `.lotpack` files - World data packages for map cells
2. `.lotheader` files - Header information for corresponding .lotpack files
3. `.bin` files (prefixed with `map_`) - Binary save game data
4. `.pack` files - Texture packs containing game graphics
5. `.tiles` files - Tile definition files
6. `.png` files - Individual texture files (when reading from directories instead of packs)

# File Contents

## .lotpack Files
- Contain map cell data in a binary format
- Each file represents a 300x300 tile section of the world
- Store basic tile information like floor types, walls, and room IDs
- Named in format `world_X_Y.lotpack` where X,Y are cell coordinates

## .lotheader Files
- Contains metadata about tile definitions used in the corresponding .lotpack file
- Includes a version number and a list of tile names
- Named in format `X_Y.lotheader` matching the lotpack coordinates
- Required to properly interpret the .lotpack data

## map_*.bin Files
- Contains save game specific data overlaid on the base map
- Includes dynamic objects like:
  - Containers and their contents
  - Zombies and their states
  - Player-built structures
  - Blood splatters
  - Vehicle data
  - Environmental changes (tree growth, erosion)
- Uses a complex binary format with version checking (supports versions 67-85)
- Named in format `map_X_Y.bin` where X,Y are coordinates

## .pack Files
- Archive files containing texture data
- Include information about sprite sheets and individual textures
- Contains image data for:
  - Terrain tiles
  - Objects
  - Characters
  - UI elements
  - Weather effects
- Each texture has associated metadata like dimensions and offsets

## .tiles Files
- Define the mapping between numeric tile IDs and texture names
- Critical for converting between binary map data and actual textures
- Contains version information and tileset definitions

## Individual .png Files
- Alternative to .pack files for texture data
- Direct image files organized in directories
- Must follow specific naming conventions to match tile definitions

# File Relationships

1. **Map Data Hierarchy**:
   - `.lotpack` files provide the base map structure
   - Each `.lotpack` requires a corresponding `.lotheader` for interpretation
   - `map_*.bin` files overlay additional game state on this base map
   - Multiple `map_*.bin` files can affect a single `.lotpack` cell

2. **Texture Resolution Chain**:
   - Map data references tiles by numeric IDs
   - `.tiles` files translate these IDs to texture names
   - Texture names are resolved to actual images via either:
     - `.pack` files containing compressed texture collections
     - Individual `.png` files in organized directories

3. **Coordinate Relationships**:
   - `.lotpack` files use a cell-based coordinate system (300x300 tiles per cell)
   - `map_*.bin` files use a chunk-based system (10x10 tiles per chunk)
   - The code includes conversion logic between these coordinate systems
   - Final output images are divided based on the user-specified divider parameter