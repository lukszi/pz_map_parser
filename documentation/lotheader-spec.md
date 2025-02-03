# Project Zomboid .lotheader File Specification

## File Contents

The .lotheader file is a binary file that contains essential metadata about tile definitions used in Project Zomboid's map system. It serves as a companion file to .lotpack files and provides the mapping information needed to interpret tile data.

Key components stored in the file:

1. **Version Number**: A 32-bit integer indicating the format version
2. **Tile Count**: A 32-bit integer specifying the total number of tile definitions
3. **Tile Definition List**: A sequence of tile name strings, with each tile's index in this list corresponding to its reference ID in the .lotpack file

The .lotheader file essentially acts as a lookup table, allowing the game and tools to translate between numeric tile IDs and their corresponding texture names.

## Binary Structure

The .lotheader file follows this binary format:

```
[Version Number] (4 bytes, Int32)
[Tile Count] (4 bytes, Int32)
[Tile Names] (Variable length sequence)
  ├─ [Tile Name 1] (Variable length string terminated by '\n')
  ├─ [Tile Name 2] (Variable length string terminated by '\n')
  └─ ... (Repeats for Tile Count entries)
```

Specific format details:
1. **Version Number**:
   - 32-bit integer in native byte order
   - Used to ensure compatibility with the reader

2. **Tile Count**:
   - 32-bit integer specifying how many tile definitions follow
   - Determines how many tile names to read

3. **Tile Names**:
   - Each tile name is stored as a sequence of characters
   - Names are terminated by a newline character ('\n')
   - No length prefix - reader must read until encountering newline
   - Each name corresponds to a texture identifier used in the game

Reading process:
1. Read first 4 bytes as version number
2. Read next 4 bytes as tile count
3. For each tile (up to tile count):
   - Read characters until encountering '\n'
   - Store complete string in tile list
   - Index in this list corresponds to tile ID in .lotpack file
