# processing/processors/tile_processor.py

import logging
from pathlib import Path
from typing import Dict, Optional

from zomboid_map_parser.io import BinaryReader
from zomboid_map_parser.models import TileDefinition
from zomboid_map_parser.parsers.tile_def_parser import TileDefParser, TileDefParserConfig


class TileProcessor:
    """
    Processes and manages tile definitions from Project Zomboid tile files.

    The TileProcessor coordinates the parsing of tile definition files and
    manages the resulting tile definitions. It maintains a collection of all
    processed tile definitions and handles the detection and logging of any
    duplicate sprite IDs that might occur across different tile files.
    """

    def __init__(self):
        """Initialize the tile processor with an empty definition store."""
        self.logger = logging.getLogger(__name__)
        self.tile_definitions: Dict[int, TileDefinition] = {}
        self._processed_files = set()

    def process_tile_file(self, file_path: Path) -> bool:
        """
        Process a single tile definition file and store its contents.

        Args:
            file_path: Path to the .tiles file to process

        Returns:
            True if processing was successful, False otherwise
        """
        if file_path in self._processed_files:
            self.logger.debug(f"Skipping already processed file: {file_path}")
            return True

        self.logger.info(f"Processing tile file: {file_path}")

        try:
            file_number = self._extract_file_number(file_path)
            config = TileDefParserConfig(
                legacy_id_mode=(file_number < 2) if file_number is not None else False
            )

            with open(file_path, 'rb') as f:
                reader = BinaryReader(f)
                parser = TileDefParser(reader, config)
                new_definitions = parser.parse()

            self._merge_definitions(new_definitions, file_path)
            self._processed_files.add(file_path)

            self.logger.info(
                f"Successfully processed {len(new_definitions)} definitions "
                f"from {file_path}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to process tile file {file_path}: {str(e)}")
            return False

    def get_definition(self, sprite_id: int) -> Optional[TileDefinition]:
        """
        Retrieve a tile definition by its sprite ID.

        Args:
            sprite_id: The unique identifier for the tile definition

        Returns:
            The TileDefinition if found, None otherwise
        """
        return self.tile_definitions.get(sprite_id)

    def get_all_definitions(self) -> Dict[int, TileDefinition]:
        """
        Retrieve all processed tile definitions.

        Returns:
            Dictionary mapping sprite IDs to their definitions
        """
        return self.tile_definitions.copy()

    def clear(self) -> None:
        """
        Clear all stored tile definitions and reset the processor state.
        """
        self.tile_definitions.clear()
        self._processed_files.clear()
        self.logger.debug("Cleared all tile definitions and processor state")

    def _extract_file_number(self, file_path: Path) -> Optional[int]:
        """
        Extract the file number from a tile definition filename.

        The file number is used to determine the sprite ID generation mode.
        Files are typically named with a number prefix, e.g., "1_tileset.tiles".

        Args:
            file_path: Path to the tile definition file

        Returns:
            The extracted file number or None if it cannot be determined
        """
        try:
            # Extract first number from filename
            file_number = int(file_path.stem.split('_')[0])
            return file_number
        except (IndexError, ValueError):
            self.logger.warning(
                f"Could not determine file number from {file_path}, "
                "defaulting to standard sprite ID generation"
            )
            return None

    def _merge_definitions(
            self,
            new_definitions: Dict[int, TileDefinition],
            source_file: Path
    ) -> None:
        """
        Merge new tile definitions with existing ones, handling duplicates.

        This method carefully merges new definitions while logging any conflicts
        that arise from duplicate sprite IDs across different files.

        Args:
            new_definitions: Dictionary of new tile definitions to merge
            source_file: Path to the source file (for conflict reporting)
        """
        for sprite_id, new_def in new_definitions.items():
            if sprite_id in self.tile_definitions:
                existing_def = self.tile_definitions[sprite_id]
                self.logger.warning(
                    f"Duplicate sprite ID {sprite_id} found in {source_file}. "
                    f"Previous definition: {existing_def.name}, "
                    f"New definition: {new_def.name}"
                )
                continue

            self.tile_definitions[sprite_id] = new_def