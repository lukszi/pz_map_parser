# io/file_manager.py
from pathlib import Path
from typing import List, Dict
import logging

from zomboid_map_parser.models import MapCell
from zomboid_map_parser.utils.exceptions import ParserError
from zomboid_map_parser.utils import CellCoord, BoundsCoord


class FileManager:
    """Handles file discovery and validation for the Project Zomboid parser."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.maps_dir = base_dir / "maps" / "Muldraugh, KY"
        self.logger = logging.getLogger(__name__)

        self._validate_directories()

    def _validate_directories(self) -> None:
        """Validate that required directories exist."""
        if not self.base_dir.exists():
            raise ParserError(f"Base directory not found: {self.base_dir}")
        if not self.maps_dir.exists():
            raise ParserError(f"Maps directory not found: {self.maps_dir}")

    def find_tile_files(self) -> List[Path]:
        """Find all .tiles files in the base directory."""
        return list(self.base_dir.glob("**/*.tiles"))

    def find_map_cells(self, bounds: BoundsCoord) -> Dict[CellCoord, MapCell]:
        """
        Find and pair all .lotheader and .lotpack files within coordinate bounds.

        Args:
            bounds: BoundsCoord object defining the search area

        Returns:
            Dictionary mapping cell coordinates to MapCell objects
        """
        cells: Dict[CellCoord, MapCell] = {}

        for header_path in self.maps_dir.glob("*.lotheader"):
            try:
                # Parse coordinates from filename (format: X_Y.lotheader)
                x, y = map(int, header_path.stem.split('_'))
                coords = CellCoord(x=x, y=y)

                # Check if coordinates are within bounds
                if not bounds.contains(coords):
                    continue

                # Look for corresponding lotpack file
                pack_path = self.maps_dir / f"world_{x}_{y}.lotpack"
                if not pack_path.exists():
                    self.logger.warning(f"Missing lotpack file for header: {header_path}")
                    continue

                # Store the cell information
                cells[coords] = MapCell(
                    coords,
                    header_path=header_path,
                    pack_path=pack_path
                )

            except ValueError:
                self.logger.error(f"Invalid filename format: {header_path}")
                continue

        return cells