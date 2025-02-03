# models/tiles/definitions.py
"""Classes for defining tile types and their properties."""

from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum
from .base import TileProperty

class TileCategory(Enum):
    """Enumeration of possible tile categories."""
    FLOOR = "floor"
    WALL = "wall"
    OBJECT = "object"
    VEGETATION = "vegetation"
    ROOF = "roof"
    FURNITURE = "furniture"

@dataclass
class TileDefinition:
    """
    Defines a type of tile and its characteristics.
    This is the template from which actual Tile instances are created.
    """
    sprite_id: int
    name: str
    tilesheet_name: str
    category: Optional[TileCategory] = None
    properties: Dict[str, TileProperty] = field(default_factory=dict)

    @property
    def full_name(self) -> str:
        """Generate the complete identifier for this tile."""
        return f"{self.tilesheet_name}_{self.name}"
