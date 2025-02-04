# processing/processors/map_processor.py

import logging
from pathlib import Path
from typing import Optional, List, Tuple

from zomboid_map_parser.io import BinaryReader
from zomboid_map_parser.models import MapCell, CellData, LotHeader
from zomboid_map_parser.parsers import LotHeaderParser, LotPackParser
from zomboid_map_parser.models.coordinates import LocalCellCoord


class MapProcessor:
    """
    Handles the processing and parsing of map cell data.

    This processor coordinates the parsing of both .lotheader and .lotpack files,
    managing the relationship between these two file types and ensuring they're
    processed in the correct order. It also handles the optional processing of
    chunk data when searching for specific tiles.

    The processor maintains minimal state, focusing instead on transforming
    input data into the appropriate model objects. This makes it easier to
    use in both single-threaded and parallel processing contexts.
    """

    def __init__(self):
        """Initialize the map processor with a configured logger."""
        self.logger = logging.getLogger(__name__)

    def parse_cell(self, cell: MapCell) -> None:
        """
        Parse a map cell's data from its associated files.

        Args:
            cell: MapCell object containing file paths and coordinates

        Updates the provided cell object directly rather than returning new data.
        """
        self.logger.info(f"Parsing map cell at coordinates {cell.coordinates}")

        try:
            # First parse the header file to get tile definitions
            header = self._parse_header(cell.header_path)
            if not header:
                self.logger.error(f"Failed to parse header for cell {cell.coordinates}")
                return

            # Use the header information to parse the pack file
            cell_data = self._parse_pack(cell.pack_path, header.tile_names)
            if not cell_data:
                self.logger.error(f"Failed to parse pack for cell {cell.coordinates}")
                return

            # Store the parsed data in the cell
            cell.header = header
            cell.data = cell_data

        except Exception as e:
            self.logger.error(
                f"Error parsing map cell {cell.coordinates}: {str(e)}"
            )

    def process_cell_for_search(
            self,
            cell: MapCell,
            tile_names_lower: List[str]
    ) -> List[Tuple[LocalCellCoord, str]]:
        """
        Process a single cell when searching for specific tiles.

        Args:
            cell: MapCell to process
            tile_names_lower: List of lowercase tile names to search for

        Returns:
            List of Tuples containing Local coordinates and tile names for found tiles
        """
        try:
            # First, only parse the header to check if any relevant tiles exist
            header = self._parse_header(cell.header_path)
            if not header:
                return []

            # Check if any of our search tiles are in this header
            header_names_lower = {name.lower() for name in header.tile_names}
            if not any(name in header_names_lower for name in tile_names_lower):
                self.logger.debug(f"Cell {cell.coordinates} does not contain searched tiles")
                return []

            # Only if we found potential matches, parse the full pack file
            cell_data = self._parse_pack(cell.pack_path, header.tile_names)
            if not cell_data:
                return []

            # Search through the cell data for matching tiles
            found_locations = []
            for z in range(8):
                for x in range(300):
                    for y in range(300):
                        pos = LocalCellCoord(x=x, y=y, z=z)
                        gs = cell_data.get_square(pos)
                        for tile_list in (gs.floor_tiles, gs.wall_tiles, gs.object_tiles):
                            for tile in tile_list:
                                if tile.texture_name.lower() in tile_names_lower:
                                    found_locations.append((pos, tile.texture_name))

            return found_locations

        except Exception as e:
            self.logger.error(
                f"Error processing cell {cell.coordinates}: {str(e)}"
            )
            return []
        finally:
            cell.header = None
            cell.data = None

    def _parse_header(self, header_path: Path) -> Optional[LotHeader]:
        """
        Parse a .lotheader file to get tile definitions.

        Args:
            header_path: Path to the .lotheader file

        Returns:
            Parsed LotHeader object or None if parsing fails
        """
        try:
            with open(header_path, 'rb') as f:
                reader = BinaryReader(f)
                parser = LotHeaderParser(reader)
                return parser.parse()
        except Exception as e:
            self.logger.error(f"Error parsing header {header_path}: {str(e)}")
            return None

    def _parse_pack(self, pack_path: Path, tile_names: List[str]) -> Optional[CellData]:
        """
        Parse a .lotpack file using tile definitions from the header.

        Args:
            pack_path: Path to the .lotpack file
            tile_names: List of tile names from the header file

        Returns:
            Parsed CellData object or None if parsing fails
        """
        try:
            with open(pack_path, 'rb') as f:
                reader = BinaryReader(f)
                parser = LotPackParser(reader, tile_names)
                return parser.parse()
        except Exception as e:
            self.logger.error(f"Error parsing pack {pack_path}: {str(e)}")
            return None