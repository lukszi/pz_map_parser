# parsers/lot_header_parser.py - Lot header parser
from typing import Optional
import logging
from dataclasses import dataclass

from zomboid_map_parser.io import BinaryReader
from zomboid_map_parser.utils.exceptions import LotHeaderParserError
from zomboid_map_parser.models import LotHeader

@dataclass
class LotHeaderParserConfig:
    """Configuration options for the lot header parser."""
    strict_mode: bool = True  # Enforce strict validation of the file format
    max_tile_count: int = 100000  # Safety limit for tile count


class LotHeaderParser:
    """
    Parses .lotheader files containing tile name mappings.

    The .lotheader format consists of:
    - Version number (4 bytes, Int32)
    - Tile count (4 bytes, Int32)
    - List of tile names (variable length strings)
    """

    def __init__(self, reader: BinaryReader, config: Optional[LotHeaderParserConfig] = None):
        """
        Initialize the parser with a binary reader and optional configuration.

        Args:
            reader: BinaryReader instance for reading the file
            config: Optional configuration settings
        """
        self.reader = reader
        self.config = config or LotHeaderParserConfig()
        self.logger = logging.getLogger(f"{__name__}.{self.reader.get_name()}")

    def _validate_tile_count(self, count: int) -> None:
        """
        Validate the tile count is within acceptable bounds.

        Args:
            count: Number of tiles specified in the header

        Raises:
            LotHeaderParserError: If tile count exceeds maximum or is negative
        """
        if count < 0:
            raise LotHeaderParserError(f"Invalid negative tile count: {count}")
        if count > self.config.max_tile_count:
            raise LotHeaderParserError(
                f"Tile count {count} exceeds maximum allowed {self.config.max_tile_count}"
            )

    def _read_tile_names(self, count: int) -> list[str]:
        """
        Read the specified number of tile names from the file.

        Args:
            count: Number of tile names to read

        Returns:
            List of tile name strings

        Raises:
            LotHeaderParserError: If there are issues reading the names
        """
        tile_names = []
        try:
            for i in range(count):
                name = self.reader.read_string()
                if not name:
                    raise LotHeaderParserError(f"Empty tile name at index {i}")
                tile_names.append(name)
        except Exception as e:
            raise LotHeaderParserError(f"Error reading tile name at index {len(tile_names)}: {str(e)}")

        return tile_names

    def parse(self) -> LotHeader:
        """
        Parse the complete lot header file.

        Returns:
            LotHeader object containing the parsed data

        Raises:
            LotHeaderParserError: If there are any parsing errors
        """
        try:
            # Read header information
            version = self.reader.read_int32(big_endian=False)
            tile_count = self.reader.read_int32(big_endian=False)

            self.logger.debug(f"Parsing lot header version {version} with {tile_count} tiles")

            # Validate tile count if in strict mode
            if self.config.strict_mode:
                self._validate_tile_count(tile_count)

            # Read all tile names
            tile_names = self._read_tile_names(tile_count)

            self.logger.debug(f"Read {len(tile_names)} tile names")
            # Create and return the header object
            return LotHeader(
                version=version,
                tile_names=tile_names,
                tile_count=tile_count
            )

        except LotHeaderParserError:
            raise  # Re-raise parser-specific errors
        except Exception as e:
            raise LotHeaderParserError(f"Unexpected error parsing lot header: {str(e)}") from e


# Example usage showing how to use the parser
def parse_lot_header(file_path: str) -> LotHeader:
    """
    Helper function to parse a lot header file from a given path.

    Args:
        file_path: Path to the .lotheader file

    Returns:
        Parsed LotHeader object
    """
    try:
        with open(file_path, 'rb') as f:
            reader = BinaryReader(f)
            parser = LotHeaderParser(reader)
            return parser.parse()
    except Exception as e:
        logging.error(f"Failed to parse lot header {file_path}: {str(e)}")
        raise

def main():
    import sys

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) != 2:
        print("Usage: python lot_header_parser.py <path_to_lotheader>")
        sys.exit(1)

    try:
        header = parse_lot_header(sys.argv[1])
        print(f"Successfully parsed lot header:")
        print(f"Version: {header.version}")
        print(f"Tile count: {header.tile_count}")
        print(f"First 5 tiles: {header.tile_names[:5]}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

# Example of processing a lot header file
if __name__ == "__main__":
    main()
