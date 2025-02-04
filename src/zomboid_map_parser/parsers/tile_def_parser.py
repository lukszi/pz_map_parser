# parsers/tile_def_parser.py - Tile definition parser
# Probably won't work, I haven't really tried to get into the tile format yet.

from typing import Dict, Optional
from dataclasses import dataclass
import logging
from pathlib import Path

from zomboid_map_parser.io import BinaryReader
from zomboid_map_parser.models import Tilesheet, TileDefinition, TileProperty
from zomboid_map_parser.utils.exceptions import TileParserError


@dataclass
class TileDefParserConfig:
    """Configuration for the tile definition parser."""
    legacy_id_mode: bool = False  # True for file numbers < 2


class TileDefParser:
    """
    Parses .tiles files containing tile definitions.
    """

    MAGIC_NUMBER = "tdef"

    def __init__(self, reader: BinaryReader, config: Optional[TileDefParserConfig] = None):
        self.reader = reader
        self.config = config or TileDefParserConfig()
        self.logger = logging.getLogger(f"{__name__}.{self.reader.get_name()}")

        # Main storage for parsed data
        self.tilesheets: Dict[str, Tilesheet] = {}
        self.tile_definitions: Dict[int, TileDefinition] = {}

        # Track the file number for ID generation
        self._file_number = self._determine_file_number()

    def _determine_file_number(self) -> int:
        """
        Determine the file number from the reader's filename if available.
        This affects how sprite IDs are generated.
        """
        try:
            if hasattr(self.reader.file, 'name'):
                filename = Path(self.reader.file.name).stem
                return int(filename.split('_')[0])
        except (AttributeError, IndexError, ValueError):
            self.logger.warning("Could not determine file number from filename")
        return 0

    def _generate_sprite_id(self, tilesheet_number: int, tile_index: int) -> int:
        """
        Generate a unique sprite ID based on file number and tile information.

        The game uses two different formulas depending on the file number:
        - For file numbers < 2: fileNumber * 100 * 1000 + 10000 + tilesetNumber * 1000 + tileIndex
        - For file numbers >= 2: fileNumber * 512 * 512 + tilesetNumber * 512 + tileIndex
        """
        if self.config.legacy_id_mode or self._file_number < 2:
            return (self._file_number * 100 * 1000 + 10000 +
                    tilesheet_number * 1000 + tile_index)
        else:
            return (self._file_number * 512 * 512 +
                    tilesheet_number * 512 + tile_index)

    def _parse_properties(self) -> Dict[str, TileProperty]:
        """Parse property key-value pairs for a tile."""
        properties = {}
        property_count = self.reader.read_int32(big_endian=False)

        for _ in range(property_count):
            name = self.reader.read_string()
            value = self.reader.read_string()
            properties[name] = TileProperty(name=name, value=value)

        return properties

    def _parse_tilesheet(self) -> Tilesheet:
        """Parse a single tilesheet definition."""
        name = self.reader.read_string()
        image_name = self.reader.read_string()
        width_tiles = self.reader.read_int32(big_endian=False)
        height_tiles = self.reader.read_int32(big_endian=False)
        tilesheet_number = self.reader.read_int32(big_endian=False)
        num_tiles = self.reader.read_int32(big_endian=False)

        self.logger.debug(f"Parsing tilesheet '{name}' with {num_tiles} tiles")

        tilesheet = Tilesheet(
            name=name,
            image_name=image_name,
            width_tiles=width_tiles,
            height_tiles=height_tiles,
            tilesheet_number=tilesheet_number
        )

        # Parse each tile in the tilesheet
        for tile_index in range(num_tiles):
            sprite_id = self._generate_sprite_id(tilesheet_number, tile_index)
            tile_name = f"{name}_{tile_index}"

            # Check for duplicate sprite IDs
            if sprite_id in self.tile_definitions:
                self.logger.warning(
                    f"Duplicate sprite ID {sprite_id} for tile {tile_name}. "
                    f"Previously defined as {self.tile_definitions[sprite_id].name}"
                )
                continue

            # Parse tile properties
            properties = self._parse_properties()

            # Create tile definition
            tile_def = TileDefinition(
                sprite_id=sprite_id,
                name=tile_name,
                tilesheet_name=name,
                properties=properties
            )

            # Store the tile definition in both collections
            tilesheet.tiles[tile_index] = tile_def
            self.tile_definitions[sprite_id] = tile_def

        return tilesheet

    def parse(self) -> Dict[int, TileDefinition]:
        """
        Parse tile definitions from the file.

        Returns:
            Dictionary mapping sprite IDs to their TileDefinitions.

        Raises:
            TileParserError: If the file format is invalid or there are parsing errors.
        """
        try:
            # Verify TDEF magic number
            self.check_magic_number()

            # Read header information
            version = self.reader.read_int32(big_endian=False)
            num_tilesheets = self.reader.read_int32(big_endian=False)

            self.logger.info(
                f"Parsing tile definitions version {version} "
                f"with {num_tilesheets} tilesheets"
            )

            # Parse each tilesheet
            for _ in range(num_tilesheets):
                tilesheet = self._parse_tilesheet()
                self.tilesheets[tilesheet.name] = tilesheet

            return self.tile_definitions

        except Exception as e:
            raise TileParserError(f"Error parsing tile definitions: {str(e)}") from e

    def check_magic_number(self):
        magic_number_bytes = self.reader.read_bytes(4)
        magic = magic_number_bytes.decode('utf-8')
        if magic != self.MAGIC_NUMBER:
            raise TileParserError(
                f"Invalid magic number: expected '{self.MAGIC_NUMBER}', got '{magic}'"
            )


# Example usage:
if __name__ == "__main__":
    import sys

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Parse a tile definition file
    filename = sys.argv[1] if len(sys.argv) > 1 else "example.tiles"

    with open(filename, "rb") as f:
        reader = BinaryReader(f)
        parser = TileDefParser(reader)

        try:
            tile_defs = parser.parse()
            print(f"Successfully parsed {len(tile_defs)} tile definitions")

            # Example: Print some tile information
            for sprite_id, tile_def in list(tile_defs.items())[:5]:
                print(f"\nSprite ID: {sprite_id}")
                print(f"Name: {tile_def.name}")
                print(f"Tilesheet: {tile_def.tilesheet_name}")
                if tile_def.properties:
                    print("Properties:")
                    for prop in tile_def.properties.values():
                        print(f"  {prop.name}: {prop.value}")

        except TileParserError as e:
            print(f"Error parsing tile definitions: {e}", file=sys.stderr)
            sys.exit(1)