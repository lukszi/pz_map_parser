# zomboid_map_parser/__init__.py
"""
Project Zomboid Map Parser
A Python library for parsing and processing Project Zomboid map files.
"""

from zomboid_map_parser.io import BinaryReader, FileManager
from zomboid_map_parser.models import CellData, GridSquare, Tile
from zomboid_map_parser.parsers import (
    TileDefParser,
    LotHeaderParser,
    LotPackParser,
)
from zomboid_map_parser.utils.coordinates import CoordinateConverter
from zomboid_map_parser.processing import Parser

__version__ = "0.1.0"
__author__ = "lukszi"

# Export main interfaces
__all__ = [
    "BinaryReader",
    "CellData",
    "GridSquare",
    "Tile",
    "TileDefParser",
    "LotHeaderParser",
    "LotPackParser",
    "CoordinateConverter",
    "Parser"
]