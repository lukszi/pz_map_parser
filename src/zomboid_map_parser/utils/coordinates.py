# utils/coordinates.py
"""
Coordinate system conversion utilities for Project Zomboid map data.

The game uses several coordinate systems:
1. World Coordinates: Global position in the game world
2. Cell Coordinates: 300x300 tile sections of the world
3. Chunk Coordinates: 10x10 tile sections within cells
4. Local Coordinates: Position within a cell or chunk

Relationships:
- Each cell is 300x300 tiles
- Each chunk is 10x10 tiles
- Each cell contains 30x30 chunks (300/10 = 30)
"""

from dataclasses import dataclass
from typing import Tuple, Optional

from zomboid_map_parser.models.coordinates import WorldCoord, CellCoord, ChunkCoord, LocalCellCoord, LocalChunkCoord


@dataclass(frozen=True)
class BoundsCoord:
    """
    Defines a rectangular boundary in the game world using cell coordinates.

    Bounds are used to limit operations to a specific area of the world map.
    The boundaries are inclusive, meaning both min and max cells are included
    in the range. A None value for any coordinate indicates no limit in that direction.

    Attributes:
        min_x: Western boundary in cell coordinates (inclusive)
        max_x: Eastern boundary in cell coordinates (inclusive)
        min_y: Southern boundary in cell coordinates (inclusive)
        max_y: Northern boundary in cell coordinates (inclusive)
    """
    min_x: Optional[int] = None
    max_x: Optional[int] = None
    min_y: Optional[int] = None
    max_y: Optional[int] = None

    def __post_init__(self):
        """Validate that the bounds are logically consistent."""
        if self.min_x is not None and self.max_x is not None:
            if self.min_x > self.max_x:
                raise ValueError(f"min_x ({self.min_x}) must be <= max_x ({self.max_x})")

        if self.min_y is not None and self.max_y is not None:
            if self.min_y > self.max_y:
                raise ValueError(f"min_y ({self.min_y}) must be <= max_y ({self.max_y})")

    def contains(self, coord: CellCoord) -> bool:
        """
        Check if a cell coordinate falls within these bounds.

        Args:
            coord: The cell coordinate to check

        Returns:
            True if the coordinate is within bounds, False otherwise
        """
        if self.min_x is not None and coord.x < self.min_x:
            return False
        if self.max_x is not None and coord.x > self.max_x:
            return False
        if self.min_y is not None and coord.y < self.min_y:
            return False
        if self.max_y is not None and coord.y > self.max_y:
            return False
        return True

    @classmethod
    def from_tuple(cls, bounds: tuple[int, int, int, int]) -> 'BoundsCoord':
        """
        Create bounds from a tuple of (min_x, max_x, min_y, max_y).

        Args:
            bounds: Tuple containing boundary values

        Returns:
            New BoundsCoord instance
        """
        min_x, max_x, min_y, max_y = bounds
        return cls(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)

    def to_tuple(self) -> tuple[Optional[int], Optional[int], Optional[int], Optional[int]]:
        """
        Convert bounds to a tuple representation.

        Returns:
            Tuple of (min_x, max_x, min_y, max_y)
        """
        return self.min_x, self.max_x, self.min_y, self.max_y

    @property
    def is_unbounded(self) -> bool:
        """Check if these bounds have any unlimited dimensions."""
        return (self.min_x is None or self.max_x is None or
                self.min_y is None or self.max_y is None)

class CoordinateConverter:
    """
    Handles conversion between different coordinate systems in Project Zomboid.

    Constants:
    - CELL_SIZE: Number of tiles in each dimension of a cell (300)
    - CHUNK_SIZE: Number of tiles in each dimension of a chunk (10)
    - CHUNKS_PER_CELL: Number of chunks in each dimension of a cell (30)
    """

    CELL_SIZE: int = 300
    CHUNK_SIZE: int = 10
    CHUNKS_PER_CELL: int = CELL_SIZE // CHUNK_SIZE  # 30

    @classmethod
    def world_to_cell(cls, coord: WorldCoord) -> Tuple[CellCoord, LocalCellCoord]:
        """
        Convert world coordinates to cell coordinates and local position.

        Takes an absolute world position and determines which cell contains it,
        along with the relative position within that cell.

        Args:
            coord: World coordinates to convert

        Returns:
            Tuple of (CellCoord, LocalCellCoord) where:
            - CellCoord is the cell containing the position
            - LocalCellCoord is the position within that cell
        """
        cell_x = coord.x // cls.CELL_SIZE
        cell_y = coord.y // cls.CELL_SIZE

        local_x = coord.x % cls.CELL_SIZE
        local_y = coord.y % cls.CELL_SIZE

        return (
            CellCoord(cell_x, cell_y),
            LocalCellCoord(local_x, local_y, coord.z)
        )

    @classmethod
    def world_to_chunk(cls, coord: WorldCoord) -> Tuple[ChunkCoord, LocalChunkCoord]:
        """
        Convert world coordinates to chunk coordinates and local position.

        Takes an absolute world position and determines which chunk contains it,
        along with the relative position within that chunk.

        Args:
            coord: World coordinates to convert

        Returns:
            Tuple of (ChunkCoord, LocalChunkCoord) where:
            - ChunkCoord is the chunk containing the position
            - LocalChunkCoord is the position within that chunk
        """
        chunk_x = coord.x // cls.CHUNK_SIZE
        chunk_y = coord.y // cls.CHUNK_SIZE

        local_x = coord.x % cls.CHUNK_SIZE
        local_y = coord.y % cls.CHUNK_SIZE

        return (
            ChunkCoord(chunk_x, chunk_y),
            LocalChunkCoord(local_x, local_y, coord.z)
        )

    @classmethod
    def cell_to_world(cls, cell: CellCoord, local: Optional[LocalCellCoord] = None) -> WorldCoord:
        """
        Convert cell coordinates and local position to world coordinates.

        Takes a cell index and a position within that cell and calculates the
        absolute world position.

        Args:
            cell: Cell coordinates
            local: Local position within the cell

        Returns:
            WorldCoord representing the absolute global position
        """
        world_x = cell.x * cls.CELL_SIZE
        world_y = cell.y * cls.CELL_SIZE
        world_z = 0
        if local:
            world_x += local.x
            world_y += local.y
            world_z = local.z

        return WorldCoord(world_x, world_y, world_z)

    @classmethod
    def chunk_to_world(cls, chunk: ChunkCoord, local: Optional[LocalChunkCoord] = None) -> WorldCoord:
        """
        Convert chunk coordinates and local position to world coordinates.

        Takes a chunk index and a position within that chunk and calculates the
        absolute world position.

        Args:
            chunk: Chunk coordinates
            local: Local position within the chunk

        Returns:
            WorldCoord representing the absolute global position
        """
        world_x = chunk.x * cls.CHUNK_SIZE
        world_y = chunk.y * cls.CHUNK_SIZE
        world_z = 0
        if local:
            world_x += local.x
            world_y += local.y
            world_z = local.z

        return WorldCoord(world_x, world_y, world_z)

    @classmethod
    def cell_to_chunks(cls, cell: CellCoord) -> Tuple[ChunkCoord, ChunkCoord]:
        """
        Get the range of chunks contained within a cell.

        Calculates the chunk coordinates for the first and last chunks in a cell,
        which can be used to iterate over all chunks in that cell.

        Args:
            cell: Cell coordinates

        Returns:
            Tuple of (start_chunk, end_chunk) representing the chunk coordinate range
        """
        start_chunk_x = cell.x * cls.CHUNKS_PER_CELL
        start_chunk_y = cell.y * cls.CHUNKS_PER_CELL

        end_chunk_x = start_chunk_x + cls.CHUNKS_PER_CELL - 1
        end_chunk_y = start_chunk_y + cls.CHUNKS_PER_CELL - 1

        return (
            ChunkCoord(start_chunk_x, start_chunk_y),
            ChunkCoord(end_chunk_x, end_chunk_y)
        )

    @classmethod
    def chunk_to_cell(cls, chunk: ChunkCoord) -> Tuple[CellCoord, LocalCellCoord]:
        """
        Convert chunk coordinates to cell coordinates and local chunk position.

        Takes a chunk index and determines which cell contains it, along with
        the chunk's relative position within that cell.

        Args:
            chunk: Chunk coordinates

        Returns:
            Tuple of (CellCoord, LocalCellCoord) where:
            - CellCoord is the cell containing the chunk
            - LocalCellCoord is the chunk's position within the cell
        """
        cell_x = chunk.x // cls.CHUNKS_PER_CELL
        cell_y = chunk.y // cls.CHUNKS_PER_CELL

        local_x = chunk.x % cls.CHUNKS_PER_CELL
        local_y = chunk.y % cls.CHUNKS_PER_CELL

        return (
            CellCoord(cell_x, cell_y),
            LocalCellCoord(local_x, local_y)
        )


def main():
    # Create a world coordinate
    world_pos = WorldCoord(x=750, y=450, z=0)

    # Convert to cell coordinates
    cell_coord, cell_local = CoordinateConverter.world_to_cell(world_pos)
    print(f"World {world_pos} is in cell {cell_coord} at local position {cell_local}")

    # Convert to chunk coordinates
    chunk_coord, chunk_local = CoordinateConverter.world_to_chunk(world_pos)
    print(f"World {world_pos} is in chunk {chunk_coord} at local position {chunk_local}")

    # Convert back to world coordinates
    world_from_cell = CoordinateConverter.cell_to_world(cell_coord, cell_local)
    print(f"Converting back to world: {world_from_cell}")

    # Get chunk range for a cell
    cell = CellCoord(2, 3)
    chunk_start, chunk_end = CoordinateConverter.cell_to_chunks(cell)
    print(f"Cell {cell} contains chunks from {chunk_start} to {chunk_end}")

# Example usage
if __name__ == "__main__":
    main()
