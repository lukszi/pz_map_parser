# zomboid_map_parser/utils/__init__.py
"""
Utility functions and helpers for coordinate conversion and data processing.

This package provides various utility functions and classes used throughout
the library, with a focus on coordinate system management and error handling.

Main Components:
- CoordinateConverter: Handles conversions between coordinate systems
- BoundsCoord: Defines rectangular boundaries in the game world
- Exceptions: Custom error types for different failure scenarios
"""

from zomboid_map_parser.utils.coordinates import (
    CoordinateConverter,
    BoundsCoord,
)
from zomboid_map_parser.utils.exceptions import (
    ParserError,
    TileParserError,
    LotHeaderParserError,
    LotPackParserError,
)

__all__ = [
    # Coordinate utilities
    "CoordinateConverter",
    "BoundsCoord",

    # Exception types
    "ParserError",
    "TileParserError",
    "LotHeaderParserError",
    "LotPackParserError",
]