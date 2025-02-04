# zomboid_map_parser/models/coordinates/relative.py
from dataclasses import dataclass


@dataclass(frozen=True)
class LocalCellCoord:
    """
    Represents a position within a specific cell relative to that cell's origin.

    Local cell coordinates measure position from the top-left corner of a cell (0,0).
    Valid coordinates range from 0-299 for both x and y within the cell.

    Attributes:
        x: X position within the cell (0-299)
        y: Y position within the cell (0-299)
        z: Height level within the cell (0-7)
    """
    x: int
    y: int
    z: int = 0


@dataclass(frozen=True)
class LocalChunkCoord:
    """
    Represents a position within a specific chunk relative to that chunk's origin.

    Local chunk coordinates measure position from the top-left corner of a chunk (0,0).
    Valid coordinates range from 0-9 for both x and y within the chunk.

    Attributes:
        x: X position within the chunk (0-9)
        y: Y position within the chunk (0-9)
        z: Height level within the chunk (0-7)
    """
    x: int
    y: int
    z: int = 0
