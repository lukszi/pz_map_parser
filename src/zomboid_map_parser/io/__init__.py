# zomboid_map_parser/io/__init__.py
"""
Input/Output utilities for handling Project Zomboid's binary file formats.

This package provides tools for reading and managing binary data from
Project Zomboid's game files, including support for different endianness
and specialized file format handling.

Main Components:
- BinaryReader: Core utility for reading binary data
- FileManager: Handles file discovery and organization
"""

from zomboid_map_parser.io.binary_reader import BinaryReader
from zomboid_map_parser.io.file_manager import FileManager

__all__ = [
    "BinaryReader",
    "FileManager",
]