# processing/core/parser.py

import logging
from pathlib import Path
from typing import Dict, List, Optional, Iterator, Union, Tuple

from ..processors import MapProcessor, TileProcessor, SearchProcessor
from ...io import FileManager
from ...models.world import MapCell
from zomboid_map_parser.utils.exceptions import ParserError
from ...utils.coordinates import (
    WorldCoord, CellCoord, LocalCellCoord, BoundsCoord,
    CoordinateConverter
)


class Parser:
    """
    Main coordinator for parsing and processing Project Zomboid map data.

    This class serves as the primary interface for map parsing operations,
    coordinating between various processors and managing the overall workflow
    of data processing. It handles the initialization and orchestration of
    specialized processors while providing a clean, high-level interface for
    clients.

    The parser maintains minimal state, primarily storing configuration and
    processor instances, while delegating actual processing work to specialized
    components. This design allows for efficient memory usage and clear
    separation of concerns.
    """

    def __init__(self, base_dir: Path, max_workers: int = 16):
        """
        Initialize the parser system.

        Args:
            base_dir: Base directory containing Project Zomboid media files
            max_workers: Maximum number of worker threads for parallel processing
        """
        self.logger = logging.getLogger(__name__)

        # Initialize core components
        self.file_manager = FileManager(base_dir)
        self.tile_processor = TileProcessor()
        self.map_processor = MapProcessor()
        self.search_processor = SearchProcessor(max_workers)

        # Map cell storage
        self._map_cells: Dict[CellCoord, MapCell] = {}

    def parse_all(
            self,
            skip_tile_parsing: bool = False,
            bounds: Optional[BoundsCoord] = None
    ) -> None:
        """
        Parse all game files within the specified bounds.

        This method coordinates the complete parsing process, handling both
        tile definitions and map data. It can optionally skip tile parsing
        if tile definitions have already been processed.

        Args:
            skip_tile_parsing: If True, skip parsing tile definition files
            bounds: Optional (min_x, max_x, min_y, max_y) for cell bounds
        """
        try:
            # Set bounds to unbounded if not provided
            if bounds is None:
                bounds = BoundsCoord()

            self.logger.info(
                "Starting complete parse operation" +
                ("" if bounds.is_unbounded else f" within bounds {bounds.to_tuple()}")
            )

            # Process tile definitions if needed
            if not skip_tile_parsing:
                self._process_tile_definitions()

            # Find and process map cells
            self._map_cells = self.file_manager.find_map_cells(bounds)
            self._process_map_cells()

            self.logger.info("Parse operation completed successfully")

        except Exception as e:
            self.logger.error(f"Error during parse operation: {str(e)}")
            raise ParserError(f"Parse operation failed: {str(e)}") from e

    def search_tiles(
            self,
            tile_names: List[str],
            parallel: bool = True,
            bounds: Optional[BoundsCoord] = None
    ) -> Iterator[Union[
        Tuple[MapCell, List[Tuple[LocalCellCoord, str]]],
        List[Tuple[MapCell, List[Tuple[LocalCellCoord, str]]]]
    ]]:
        """
        Search for specific tiles across map cells.

        This method provides flexible search capabilities, supporting both
        parallel and sequential processing approaches. It can also limit
        the search to specific map bounds.

        Args:
            tile_names: List of tile names to search for
            parallel: Whether to use parallel processing
            bounds: Optional coordinate bounds for the search

        Yields:
            Search results in either single or batch format depending on
            the parallel parameter
        """
        # Update bounds if specified
        if bounds is not None:
            self._map_cells = self.file_manager.find_map_cells(bounds)

        # Choose search method based on parallel flag
        if parallel:
            yield from self.search_processor.search_tiles_parallel(
                self._map_cells,
                tile_names
            )
        else:
            yield from self.search_processor.search_tiles(
                self._map_cells,
                tile_names
            )

    def get_cell_at_world_position(self, position: WorldCoord) -> Optional[MapCell]:
        """
        Get the map cell containing the specified world position.

        Args:
            position: World coordinates to look up

        Returns:
            MapCell if found at the position, None otherwise
        """
        cell_coord, _ = CoordinateConverter.world_to_cell(position)
        return self._map_cells.get(cell_coord)

    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about the parsed data.

        Returns:
            Dictionary containing various processing statistics
        """
        stats = {
            'map_cells': len(self._map_cells),
            # 'tile_definitions': len(self.tile_processor.get_all_definitions()),
        }

        # Add search statistics if available
        search_stats = self.search_processor.get_statistics()
        stats.update(search_stats)

        return stats

    def clear_data(self) -> None:
        """
        Clear all loaded data to free memory.

        This method provides a way to release memory when processing is complete
        or when preparing for a new processing operation.
        """
        self.tile_processor.clear()
        self._map_cells.clear()

    def _process_tile_definitions(self) -> None:
        """Process all tile definition files in the game directory."""
        tile_files = self.file_manager.find_tile_files()

        self.logger.info(f"Processing {len(tile_files)} tile definition files")
        for tile_file in tile_files:
            if not self.tile_processor.process_tile_file(tile_file):
                self.logger.warning(f"Failed to process tile file: {tile_file}")

    def _process_map_cells(self) -> None:
        """Process all discovered map cells."""
        self.logger.info(f"Processing {len(self._map_cells)} map cells")

        for cell in self._map_cells.values():
            try:
                self.map_processor.parse_cell(cell)
            except Exception as e:
                self.logger.error(
                    f"Failed to process cell {cell.coordinates}: {str(e)}"
                )