# zomboid_map_parser/models/tiles/__init__.py
"""
Tile-related models and definitions for Project Zomboid map data.

This package provides data structures for representing individual tiles,
their properties, and collections of tiles. It includes both definition
models used for tile types and instance models for placed tiles.

Main Components:
- Basic Tile Models: Individual tiles and their properties
- Tile Definitions: Templates and categories for tile types
- Tile Collections: Groups and containers of related tiles
"""

from zomboid_map_parser.models.tiles.base import (
    Tile,
    TileProperty,
)
from zomboid_map_parser.models.tiles.definitions import (
    TileDefinition,
    TileCategory,
)
from zomboid_map_parser.models.tiles.containers import (
    Tilesheet,
    LotHeader,
)

__all__ = [
    # Basic tile models
    "Tile",
    "TileProperty",

    # Tile type definitions
    "TileDefinition",
    "TileCategory",

    # Tile collections
    "Tilesheet",
    "LotHeader",
]