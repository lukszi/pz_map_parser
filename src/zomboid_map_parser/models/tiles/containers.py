# models/tiles/containers.py
"""Container classes that group related tile information."""

from dataclasses import dataclass, field
from typing import Dict, List
from .definitions import TileDefinition

@dataclass
class Tilesheet:
    """
    Represents a collection of related tiles.
    Tilesheets are the primary way tiles are organized in the game's assets.
    """
    name: str
    image_name: str
    width_tiles: int
    height_tiles: int
    tilesheet_number: int
    tiles: Dict[int, TileDefinition] = field(default_factory=dict)

    def add_tile(self, index: int, tile: TileDefinition) -> None:
        """Add a tile definition to this tilesheet."""
        self.tiles[index] = tile

    def get_tile(self, index: int) -> TileDefinition:
        """Retrieve a tile definition by its index."""
        return self.tiles[index]

@dataclass
class LotHeader:
    """
    Contains tile mapping information for a specific lot/cell.
    This acts as a lookup table between tile IDs and names.
    """
    version: int
    tile_names: List[str]
    tile_count: int

    @property
    def tile_mapping(self) -> Dict[int, str]:
        """Create a mapping of indices to tile names."""
        return {idx: name for idx, name in enumerate(self.tile_names)}
