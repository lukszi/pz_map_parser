# processing/processors/search_processor.py

import logging
from typing import Dict, List, Iterator

from zomboid_map_parser.processing.parallel import BatchProcessor, BatchProcessingConfig
from zomboid_map_parser.models.world import MapCell
from zomboid_map_parser.processing.processors.map_processor import MapProcessor
from zomboid_map_parser.models.coordinates import LocalCellCoord, CellCoord


class SearchProcessor:
    """
    Handles searching for specific tiles across map cells.

    This processor coordinates the searching of tile patterns across multiple
    map cells, supporting both sequential and parallel processing approaches.
    It works in conjunction with the MapProcessor to load and analyze cell
    data efficiently.
    """

    def __init__(self, max_workers: int = 4):
        """Initialize the search processor with specified parallelism."""
        self.logger = logging.getLogger(__name__)
        self.map_processor = MapProcessor()
        self.batch_processor = BatchProcessor(BatchProcessingConfig(
            max_workers=max_workers,
            batch_size=4,
            retry_count=3,
            log_progress=True
        ))

    def search_tiles(
            self,
            cells: Dict[CellCoord, MapCell],
            tile_names: List[str]
    ) -> Iterator[tuple[MapCell, List[tuple[LocalCellCoord, str]]]]:
        """
        Search for specific tiles across map cells sequentially.

        Args:
            cells: Dictionary of map cells to search
            tile_names: List of tile names to search for

        Yields:
            Tuples of (MapCell, list of found tile locations)
        """
        tile_names_lower = [name.lower() for name in tile_names]

        for cell in cells.values():
            try:
                found_locations = self.map_processor.process_cell_for_search(
                    cell,
                    tile_names_lower
                )

                if found_locations:
                    yield cell, found_locations

            except Exception as e:
                self.logger.error(
                    f"Error searching cell {cell.coordinates}: {str(e)}"
                )

    def search_tiles_parallel(
            self,
            cells: Dict[CellCoord, MapCell],
            tile_names: List[str],
    ) -> Iterator[List[tuple[MapCell, List[tuple[LocalCellCoord, str]]]]]:
        """
        Search for tiles across cells in parallel batches.

        Args:
            cells: Dictionary of map cells to search
            tile_names: List of tile names to search for

        Yields:
            Lists of (MapCell, found tile locations) for each batch
        """
        tile_names_lower = [name.lower() for name in tile_names]

        def process_cell(
                cell: MapCell
        ) -> tuple[MapCell, list[tuple[LocalCellCoord, str]]]:
            """Process a single cell for batch processing."""
            found_locations = self.map_processor.process_cell_for_search(
                cell,
                tile_names_lower
            )
            return cell, found_locations

        yield from self.batch_processor.process_items(
            items=list(cells.values()),
            process_func=process_cell,
            filter_func=lambda result: bool(result[1])
        )

    def get_statistics(self) -> dict:
        """Get search processing statistics."""
        return self.batch_processor.get_statistics()