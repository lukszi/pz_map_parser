from dataclasses import dataclass


@dataclass(frozen=True)
class WorldCoord:
    """
    Represents an absolute position in the game world.

    World coordinates measure individual tile positions from a global origin point (0,0,0).
    This is the most precise coordinate system and can identify any tile in the game world.

    Attributes:
        x: Global X position in tiles, measured from world origin
        y: Global Y position in tiles, measured from world origin
        z: Height level (0-7, where 0 is ground level)
    """
    x: int
    y: int
    z: int = 0


@dataclass(frozen=True)
class CellCoord:
    """
    Represents a 300x300 tile section of the world map.

    Cell coordinates identify major divisions of the world map. Each cell corresponds to
    a pair of .lotpack/.lotheader files that store the map data for that section.
    Cell (0,0) contains world coordinates (0-299, 0-299).

    Attributes:
        x: Cell X index, where each increment represents 300 tiles
        y: Cell Y index, where each increment represents 300 tiles
    """
    x: int
    y: int


@dataclass(frozen=True)
class ChunkCoord:
    """
    Represents a 10x10 tile section within the world.

    Chunk coordinates identify smaller sections used for efficient memory management
    and data processing. Each cell contains 30x30 chunks (900 total chunks per cell).
    Chunk (0,0) contains world coordinates (0-9, 0-9).

    Attributes:
        x: Chunk X index, where each increment represents 10 tiles
        y: Chunk Y index, where each increment represents 10 tiles
    """
    x: int
    y: int
