# Project Zomboid .lotpack File Specification

## File Contents

The .lotpack file is a binary file format used by Project Zomboid to store map cell data. Each .lotpack file represents a 300x300 tile section of the game world and contains fundamental map information.

Key components stored in the file:

1. **Map Cell Data**: Basic information about a 300x300 section including:
   - Floor types
   - Wall placements
   - Room IDs and definitions
   - Ground textures and overlays
   - Basic structure definitions

2. **Chunk Organization**:
   - The 300x300 area is divided into chunks
   - Each chunk contains data for multiple z-levels (floors/heights)
   - Contains flags for occupied/empty spaces
   - Stores room associations and connections

3. **Environmental Information**:
   - Basic terrain data
   - Room definitions and boundaries
   - Static object placements
   - Initial state of built structures

Note that .lotpack files contain only the base map data - dynamic elements like containers, zombies, and player constructions are stored separately in .bin files.

## Binary Structure

The .lotpack file follows this binary format:

```
[File Header]
├─ [Chunk Count] (4 bytes)
├─ [Chunk Offsets] (Array of offsets)
│  ├─ [Offset] (4 bytes)
│  └─ [0x00 Padding] (4 bytes)

[Chunk Data] (Repeated for each chunk)
├─ [Z-levels] (8 levels)
│  ├─ [Tile Data]
│  │  ├─ [Count] (4 bytes)
│  │  ├─ [Room ID] (4 bytes, if count > 1)
│  │  └─ [Tile IDs] (Array of 4-byte IDs)
│  └─ [Skip Count] (4 bytes, -1 if skipping)
└─ [End Marker]
```

Specific format details:

1. **File Header**:
   - First 4 bytes: Total number of chunks
   - Followed by an array of 32-bit offsets pointing to chunk data padded with 4 bytes of 0
   - Each offset indicates where the corresponding chunk's data begins

2. **Chunk Organization**:
   - Each chunk represents a 10x10 tile area
   - File contains 30x30 chunks (total 300x300 tiles)
   - Chunks are ordered row by row, left to right

3. **Z-Level Data**:
   - Each chunk contains 8 z-levels (floors/heights)
   - Z-levels are stored sequentially
   - Empty z-levels are marked with skip counts

4. **Tile Data Format**:
   - Count field indicates number of tiles in sequence
   - If count > 1, includes room ID
   - Followed by array of tile IDs
   - Tile IDs correspond to definitions in .lotheader file

5. **Skip Mechanism**:
   - Uses -1 count to indicate skipped tiles
   - Following 4 bytes indicate number of tiles to skip
   - Optimizes storage of empty spaces
