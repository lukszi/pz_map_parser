# zomboid_map_parser/__init__.py
"""
Project Zomboid Map Parser
A Python library for parsing and processing Project Zomboid map files.

This library provides tools for reading, parsing, and analyzing map data from
Project Zomboid game files. It handles various coordinate systems, tile definitions,
and map cell data while providing both high-level and low-level interfaces for
working with the game's map format.

Main Components:
- Parser: High-level interface for parsing map data
- Coordinate Systems: Tools for working with different map coordinate spaces
- Models: Data structures representing game map elements
- File Handling: Utilities for reading game data files
"""

from zomboid_map_parser.processing import Parser
from zomboid_map_parser.models import (
    WorldCoord, CellCoord, ChunkCoord,
    LocalCellCoord, LocalChunkCoord,
    GridSquare, CellData, MapCell,
    Tile, TileDefinition, Tilesheet
)
from zomboid_map_parser.utils import CoordinateConverter, BoundsCoord

__version__ = "0.1.0"
__author__ = "lukszi"

__all__ = [
    # Main parser interface
    "Parser",

    # Core coordinate types
    "WorldCoord",
    "CellCoord",
    "ChunkCoord",
    "LocalCellCoord",
    "LocalChunkCoord",

    # Map data structures
    "GridSquare",
    "CellData",
    "MapCell",

    # Tile-related classes
    "Tile",
    "TileDefinition",
    "Tilesheet",

    # Utility classes
    "CoordinateConverter",
    "BoundsCoord",
]