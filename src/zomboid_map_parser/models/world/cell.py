# models/cell.py
from typing import Dict

from .grid import GridSquare
from zomboid_map_parser.models.coordinates import LocalCellCoord


class CellData:
    """Manages a 3D array of GridSquares representing a map cell."""

    def __init__(self):
        # Initialize 3D array (8 levels, 300x300 squares)
        self.squares: Dict[LocalCellCoord, GridSquare] = {}

    def get_square(self, position: LocalCellCoord, create_if_not_exists: bool = False) -> GridSquare:
        """Get the GridSquare at the specified coordinates."""
        square = self.squares.get(position, None)

        # Create empty square if not found
        if square is None:
            square = GridSquare(position)
            # Add square to storage if requested
            if create_if_not_exists:
                self.squares[position] = square
        return square