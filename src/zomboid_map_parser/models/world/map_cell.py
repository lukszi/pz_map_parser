# models/map_cell.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .cell import CellData
from ..tiles.containers import LotHeader
from ...utils import LocalCellCoord, CellCoord, CoordinateConverter


@dataclass
class MapCell:
    """
    Represents a cell in the game map with its associated files and data.

    A MapCell ties together the physical files (.lotheader and .lotpack) with their
    parsed data structures. This creates a complete representation of a map cell
    that includes both its raw files and processed content.
    """
    position: CellCoord
    header_path: Path  # Path to .lotheader file
    pack_path: Path   # Path to .lotpack file
    header: Optional[LotHeader] = None  # Parsed header data
    data: Optional[CellData] = None    # Parsed cell data

    @property
    def coordinates(self) -> CellCoord:
        """Get the cell's coordinates."""
        return self.position

    @property
    def is_loaded(self) -> bool:
        """Check if both header and data have been parsed."""
        return self.header is not None and self.data is not None

    @property
    def tile_count(self) -> int:
        """Get the total number of tiles in this cell."""
        if not self.data:
            return 0

        count = 0
        cell_size = CoordinateConverter.CELL_SIZE
        for z in range(8):  # 8 z-levels
            for x in range(cell_size):
                for y in range(cell_size):
                    gs = self.data.get_square(LocalCellCoord(x, y, z))
                    count += (len(gs.floor_tiles) +
                            len(gs.wall_tiles) +
                            len(gs.object_tiles))
        return count