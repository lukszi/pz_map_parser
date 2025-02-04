# zomboid_map_parser/models/world/__init__.py
"""
World structure models for Project Zomboid map data.

This package provides data structures for representing the organization of
the game world, from individual grid squares up to complete map cells. These
models form the core hierarchy of how map data is stored and accessed.

Main Components:
- GridSquare: Individual positions in the game world
- CellData: Collections of grid squares forming a map cell
- MapCell: Complete cell data including file references
"""

from zomboid_map_parser.models.world.grid import GridSquare
from zomboid_map_parser.models.world.cell import CellData
from zomboid_map_parser.models.world.map_cell import MapCell

__all__ = [
    "GridSquare",
    "CellData",
    "MapCell",
]