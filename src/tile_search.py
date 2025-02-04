import math
from pathlib import Path
import logging
from typing import Iterator, Tuple, List, Union

from zomboid_map_parser import CoordinateConverter
from zomboid_map_parser.processing import Parser
from zomboid_map_parser.models import MapCell
from zomboid_map_parser.utils import BoundsCoord
from zomboid_map_parser.models.coordinates.relative import LocalCellCoord
from zomboid_map_parser.models.coordinates.absolute import WorldCoord


def search_world_for_tile(
        game_dir: Path,
        tile_name: Union[str, List[str]],
        bounds: BoundsCoord = None,
        parallel: bool = True
) -> Iterator[Tuple[MapCell, list[tuple[LocalCellCoord, str]]]]:
    """
    Search the world for specific tiles using the existing project architecture.

    Args:
        game_dir: Path to Project Zomboid media directory
        tile_name: Name of the tile to search for or list of names
        bounds: Optional (min_x, max_x, min_y, max_y) to limit search area
        parallel: Whether to use parallel processing

    Yields:
        Tuples of (MapCell, list of found tile locations)
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        # Initialize the main parser
        parser = Parser(game_dir)

        # Perform the search using the existing search processor
        logger.info(f"Searching for tile: {tile_name}")
        results = parser.search_tiles(
            tile_names=[tile_name] if isinstance(tile_name, str) else tile_name,
            parallel=parallel,
            bounds=bounds
        )

        # Yield results as they're found
        for batch in results:
            if isinstance(batch, list):
                # In parallel mode, results come in batches
                for cell, locations in batch:
                    if locations:
                        yield cell, locations
            else:
                # In sequential mode, results come one at a time
                cell, locations = batch
                if locations:
                    yield cell, locations

    except Exception as e:
        logger.error(f"Error during tile search: {str(e)}")
        raise


def main():
    # Example usage
    game_dir = Path("K:\\SteamLibrary\\steamapps\\common\\ProjectZomboid\\media")
    popsicle_fridge_names = [
        "appliances_refrigeration_01_20",
        "appliances_refrigeration_01_21",
        "appliances_refrigeration_01_38",
        "appliances_refrigeration_01_39"
    ]

    # Optional: limit search to specific area
    bounds = BoundsCoord(None, None, None, None)
    finds_per_cell: List[Tuple[MapCell,  list[tuple[LocalCellCoord, str]]]] = []
    try:
        # Perform search
        found_count = 0
        total_locations = 0

        for cell, locations in search_world_for_tile(
                game_dir,
                popsicle_fridge_names,
                bounds=bounds,
                parallel=True
        ):
            found_count += 1
            total_locations += len(locations)
            finds_per_cell.append((cell, locations))

        for cell, locations in finds_per_cell:
            print(f"\nFound in cell {cell.coordinates}:")
            for cell_coord, name in locations:
                world_coord = CoordinateConverter.cell_to_world(cell.coordinates, cell_coord)
                print(f"\t{name}: cell={cell_coord}, world={world_coord}")

        print(f"\nSummary:")
        print(f"Found {total_locations} instances")
        print(f"Across {found_count} cells")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()