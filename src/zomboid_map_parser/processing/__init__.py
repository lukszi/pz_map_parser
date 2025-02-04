# zomboid_map_parser/processing/__init__.py
"""
Processing components for parsing and analyzing Project Zomboid map data.

This package provides the main processing infrastructure for working with
map data, including the high-level Parser interface and specialized processors
for different aspects of the map data.

Main Components:
- Parser: Primary interface for parsing and processing map data
- Processors: Specialized components for different processing tasks
- Parallel Processing: Tools for handling large-scale data processing
"""

from zomboid_map_parser.processing.core import Parser
from zomboid_map_parser.processing.processors import (
    MapProcessor,
    TileProcessor,
    SearchProcessor,
)
from zomboid_map_parser.processing.parallel import (
    BatchProcessor,
    BatchProcessingConfig,
)

__all__ = [
    # Main parser interface
    "Parser",

    # Specialized processors
    "MapProcessor",
    "TileProcessor",
    "SearchProcessor",

    # Parallel processing tools
    "BatchProcessor",
    "BatchProcessingConfig",
]