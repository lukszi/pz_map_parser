# models/grid.py
from typing import List, Optional

from zomboid_map_parser.models.tiles import Tile
from zomboid_map_parser.utils.coordinates import LocalChunkCoord, LocalCellCoord


class GridSquare:
    """Represents a single square in the game map with multiple layers."""

    def __init__(self, position: LocalChunkCoord | LocalCellCoord):
        self.position = position
        self.floor_tiles: List[Tile] = []
        self.wall_tiles: List[Tile] = []
        self.object_tiles: List[Tile] = []
        self.room_id: Optional[int] = None

    def add_tile(self, layer: int, tile: Tile):
        """Add a tile to the specified layer."""
        if layer == 0:  # FLOOR
            self.floor_tiles.append(tile)
        elif layer == 1:  # WALL
            self.wall_tiles.append(tile)
        elif layer == 2:  # OBJECT
            self.object_tiles.append(tile)
