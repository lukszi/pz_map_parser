# processing/__init__.py
"""
Processing package for the Project Zomboid map parser.

This package coordinates the parsing and processing of Project Zomboid map data,
providing a high-level interface through the Parser class while managing the
complexities of file processing, tile management, and search operations through
specialized components.
"""

from zomboid_map_parser.processing.core.parser import Parser
from zomboid_map_parser.processing.parallel import BatchProcessor, BatchProcessingConfig

__all__ = [
    "Parser",
    "BatchProcessor",
    "BatchProcessingConfig"
]