# parsers/lot_pack_parser.py

from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

from ..io import BinaryReader
from ..models import CellData, Tile
from zomboid_map_parser.utils.exceptions import LotPackParserError
from ..utils.coordinates import (
    ChunkCoord, LocalCellCoord,
    CoordinateConverter
)


@dataclass
class ChunkOffset:
    """Represents an offset to chunk data in the lotpack file."""
    position: int
    size: Optional[int] = None


class LotPackParser:
    """
    Parses .lotpack files containing map cell data.

    The .lotpack format organizes data in a hierarchical structure:
    - Each file represents a 300x300 cell
    - Cells are divided into 30x30 chunks
    - Each chunk contains 10x10 tiles
    - Each position can have up to 8 z-levels (heights)

    The parser uses the coordinate system classes to handle translations between
    these different coordinate spaces correctly.
    """

    def __init__(self, reader: BinaryReader, tile_names: List[str]):
        """
        Initialize the parser.

        Args:
            reader: BinaryReader instance for reading the file
            tile_names: List of tile names from the corresponding .lotheader file
        """
        self.reader = reader
        self.tile_names = tile_names
        self.logger = logging.getLogger(f"{__name__}.{self.reader.get_name()}")

        # Main storage for parsed data
        self.cell_data = CellData()

        # Track chunk offsets using proper coordinate system
        self.chunk_offsets: Dict[ChunkCoord, ChunkOffset] = {}
        self.current_chunk: Optional[ChunkCoord] = None

    def _read_chunk_offsets(self):
        """
        Read the chunk offset table from the file header.

        The file starts with a table of offsets pointing to where each chunk's
        data begins in the file. This allows for random access to chunk data.
        """
        # First 4 bytes contain the number of chunks
        chunk_count = self.reader.read_int32(big_endian=False)
        self.logger.debug(f"Reading offsets for {chunk_count} chunks")
        if chunk_count != CoordinateConverter.CHUNKS_PER_CELL ** 2:
            self.logger.warning(f"Unexpected chunk count: {chunk_count}")

        # Read offset for each chunk in the 30x30 chunk grid
        for cx in range(CoordinateConverter.CHUNKS_PER_CELL):
            for cy in range(CoordinateConverter.CHUNKS_PER_CELL):
                pos = self.reader.read_int32(big_endian=False)
                _0_padding = self.reader.read_int32(big_endian=False)
                if _0_padding != 0:
                    self.logger.warning(f"Unexpected padding value: {_0_padding}")
                if pos > 0:  # Valid chunk position
                    chunk_coord = ChunkCoord(cx, cy)
                    self.chunk_offsets[chunk_coord] = ChunkOffset(position=pos)

    def _read_tile_sequence(self, position: LocalCellCoord) -> Optional[int]:
        """
        Read a sequence of tiles for a specific position.

        Args:
            position: Local coordinates within the cell for this tile sequence
        """
        # Get count of tiles at this position
        count = self.reader.read_int32(big_endian=False)

        if count == -1:  # Skip marker
            skip_count = self.reader.read_int32(big_endian=False)
            return skip_count-1

        if count <= 0:
            return  # No tiles to process

        # If there are tiles, first value is room ID
        room_id = self.reader.read_int32(big_endian=False) if count > 1 else None

        # Get the grid square for this position
        gs = self.cell_data.get_square(position, create_if_not_exists=True)
        if room_id is not None:
            gs.room_id = room_id

        # Read each tile definition
        for _ in range(1, count):
            tile_id = self.reader.read_int32(big_endian=False)

            # Convert tile ID to name using the lookup from .lotheader
            if 0 <= tile_id < len(self.tile_names):
                tile_name = self.tile_names[tile_id]

                # Create tile instance
                tile = Tile(
                    tile_id=tile_id,
                    texture_name=tile_name
                )

                # Add to appropriate layer based on tile type
                if "wall" in tile_name.lower():
                    gs.add_tile(1, tile)  # Wall layer
                elif "floor" in tile_name.lower():
                    gs.add_tile(0, tile)  # Floor layer
                else:
                    gs.add_tile(2, tile)  # Object layer

    def _parse_chunk(self, chunk_coord: ChunkCoord) -> None:
        """
        Parse data for a specific chunk.

        Args:
            chunk_coord: Coordinates of the chunk to parse
        """
        self.current_chunk = chunk_coord
        chunk_offset = self.chunk_offsets.get(chunk_coord)

        if not chunk_offset:
            return  # Skip empty chunks

        # Position reader at chunk data
        self.reader.file.seek(chunk_offset.position)

        # Calculate base coordinates for this chunk
        chunk_base_x = chunk_coord.x * CoordinateConverter.CHUNK_SIZE
        chunk_base_y = chunk_coord.y * CoordinateConverter.CHUNK_SIZE

        # Process each position in the chunk
        skip_count = 0
        for z in range(8):  # 8 z-levels
            for x in range(CoordinateConverter.CHUNK_SIZE):  # 10x10 tiles per chunk
                for y in range(CoordinateConverter.CHUNK_SIZE):
                    # Skip tiles if skip count active
                    if skip_count > 0:
                        skip_count -= 1
                        continue
                    # Convert chunk-local coordinates to cell-local coordinates
                    pos_in_cell = LocalCellCoord(
                        x=chunk_base_x + x,
                        y=chunk_base_y + y,
                        z=z
                    )
                    res = self._read_tile_sequence(pos_in_cell)
                    skip_count = res if res is not None else 0

    def parse(self) -> CellData:
        """
        Parse the complete lotpack file.

        Returns:
            CellData object containing the parsed map data

        Raises:
            LotPackParserError: If there are any parsing errors
        """
        try:
            # Read chunk offset table
            self._read_chunk_offsets()

            # Process each chunk using proper coordinate system
            for cx in range(CoordinateConverter.CHUNKS_PER_CELL):
                for cy in range(CoordinateConverter.CHUNKS_PER_CELL):
                    chunk_coord = ChunkCoord(cx, cy)
                    self._parse_chunk(chunk_coord)

            self.logger.info(f"Parsed {len(self.cell_data.squares)} grid squares")
            return self.cell_data

        except Exception as e:
            raise LotPackParserError(
                f"Error parsing chunk {self.current_chunk}: {str(e)}"
            ) from e


# Helper function showing how to parse a lotpack file
def parse_lot_pack(file_path: str, tile_names: List[str]) -> CellData:
    """
    Parse a lotpack file from a given path.

    Args:
        file_path: Path to the .lotpack file
        tile_names: List of tile names from corresponding .lotheader

    Returns:
        Parsed CellData object
    """
    try:
        with open(file_path, 'rb') as f:
            reader = BinaryReader(f)
            parser = LotPackParser(reader, tile_names)
            return parser.parse()
    except Exception as e:
        logging.error(f"Failed to parse lotpack {file_path}: {str(e)}")
        raise


def main():
    import sys

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) != 3:
        print("Usage: python lot_pack_parser.py <path_to_lotpack> <path_to_lotheader>")
        sys.exit(1)

    try:
        # First parse the lotheader to get tile names
        from .lot_header_parser import parse_lot_header
        header = parse_lot_header(sys.argv[2])

        # Then parse the lotpack
        cell_data = parse_lot_pack(sys.argv[1], header.tile_names)

        print(f"Successfully parsed lotpack file")
        # Print some statistics about the parsed data
        total_tiles = sum(
            len(gs.floor_tiles) + len(gs.wall_tiles) + len(gs.object_tiles)
            for z in range(8)
            for x in range(CoordinateConverter.CELL_SIZE)
            for y in range(CoordinateConverter.CELL_SIZE)
            if (gs := cell_data.get_square(LocalCellCoord(x, y, z)))
        )
        print(f"Total tiles parsed: {total_tiles}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()