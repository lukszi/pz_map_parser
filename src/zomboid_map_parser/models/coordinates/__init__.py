# zomboid_map_parser/models/coordinates/__init__.py
"""
Coordinate system models for Project Zomboid map data.

This package provides data structures for representing positions in different
coordinate systems used by Project Zomboid. It includes both absolute world
coordinates and relative positioning within cells and chunks.

Main Components:
- Absolute Coordinates: World, cell, and chunk positions
- Relative Coordinates: Local positions within cells and chunks
"""

from zomboid_map_parser.models.coordinates.absolute import (
    WorldCoord,
    CellCoord,
    ChunkCoord,
)
from zomboid_map_parser.models.coordinates.relative import (
    LocalCellCoord,
    LocalChunkCoord,
)

__all__ = [
    # Absolute coordinate types
    "WorldCoord",
    "CellCoord",
    "ChunkCoord",

    # Relative coordinate types
    "LocalCellCoord",
    "LocalChunkCoord",
]