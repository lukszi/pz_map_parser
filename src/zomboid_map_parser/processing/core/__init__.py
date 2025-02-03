# processing/core/__init__.py
"""
Core processing components for the Project Zomboid map parser.

This package contains the main parser class that orchestrates the overall
processing operations, serving as the primary entry point for map parsing
and analysis operations.
"""

from .parser import Parser

__all__ = ["Parser"]