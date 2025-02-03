# models/tiles/base.py
"""Base classes for tile representation."""

from dataclasses import dataclass

@dataclass
class TileProperty:
    """
    Represents a property associated with a tile.
    These properties define behavior and appearance in the game.
    """
    name: str
    value: str

@dataclass
class Tile:
    """
    Represents a specific instance of a tile in the game world.
    This is used for actual tile placement rather than definition.
    """
    tile_id: int
    texture_name: str
    offset_x: int = 0
    offset_y: int = 0
    properties: dict[str, TileProperty] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
