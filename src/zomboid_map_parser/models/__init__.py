# zomboid_map_parser/models/__init__.py
"""
Data models for Project Zomboid map structures and game elements.

This package provides data structures for representing various aspects of
Project Zomboid's map system. Models are organized hierarchically to represent
different levels of the game world, from individual tiles to complete map cells.

Main Components:
- Coordinate Models: Different coordinate systems used in the game
- Tile Models: Representation of individual tiles and their properties
- Grid Models: Structures for organizing tiles in the game world
- Cell Models: Large-scale map organization
"""

from zomboid_map_parser.models.coordinates import (
    WorldCoord,
    CellCoord,
    ChunkCoord,
    LocalCellCoord,
    LocalChunkCoord,
)
from zomboid_map_parser.models.tiles import (
    Tile,
    TileProperty,
    TileDefinition,
    TileCategory,
    Tilesheet,
    LotHeader,
)
from zomboid_map_parser.models.world import (
    GridSquare,
    CellData,
    MapCell,
)

__all__ = [
    # Coordinate models
    "WorldCoord",
    "CellCoord",
    "ChunkCoord",
    "LocalCellCoord",
    "LocalChunkCoord",

    # Tile models
    "Tile",
    "TileProperty",
    "TileDefinition",
    "TileCategory",
    "Tilesheet",
    "LotHeader",

    # World structure models
    "GridSquare",
    "CellData",
    "MapCell",
]