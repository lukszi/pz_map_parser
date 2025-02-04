# models/__init__.py
"""
Data models for Project Zomboid map structures and game elements.

This package provides a comprehensive set of data structures for representing
various aspects of Project Zomboid's map system, from individual tiles to
complete map cells. The models are organized hierarchically, with clear
separation between different concerns:

Core Components:
    - Tile-related classes (Tile, TileDefinition, Tilesheet)
    - Map structure classes (GridSquare, CellData)
    - Property and metadata classes (TileProperty)

Usage:
    from zomboid_map_parser.models import Tile, GridSquare, CellData
    from zomboid_map_parser.models.tiles import TileDefinition, Tilesheet
"""

# Import all tile-related models through the tiles subpackage
from .tiles import (
    Tile,
    TileProperty,
    TileDefinition,
    TileCategory,
    Tilesheet,
    LotHeader
)

# Import the grid and cell models
from .world import GridSquare, MapCell, CellData

# Import all the coordinate models
from .coordinates import (
    WorldCoord,
    CellCoord,
    ChunkCoord,

    LocalCellCoord,
    LocalChunkCoord
)

# Define what symbols should be available when using 'from models import *'
__all__ = [
    # Core map structures
    "GridSquare",
    "CellData",
    "MapCell",

    # Tile-related classes
    "Tile",
    "TileProperty",
    "TileDefinition",
    "TileCategory",
    "Tilesheet",
    "LotHeader",

    # Coordinate classes
    "WorldCoord",
    "CellCoord",
    "ChunkCoord",
    "LocalCellCoord",
    "LocalChunkCoord"
]