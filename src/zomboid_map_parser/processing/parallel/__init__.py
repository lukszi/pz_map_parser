# processing/parallel/__init__.py
"""
Utilities for parallel processing of map data.

This package provides tools and utilities for handling parallel processing
operations, particularly focused on batch processing of large datasets in
a memory-efficient manner.
"""

from zomboid_map_parser.processing.parallel.batch_processor import BatchProcessor, BatchProcessingConfig

__all__ = [
    "BatchProcessor",
    "BatchProcessingConfig"
]