# exceptions.py
class ParserError(Exception):
    """Base class for parser-related exceptions."""
    pass

class TileParserError(ParserError):
    """Raised when there is an error parsing tile definitions."""
    pass

class LotHeaderParserError(ParserError):
    """Raised when there are issues parsing a lot header file."""
    pass

class LotPackParserError(ParserError):
    """Raised when there are issues parsing a lot pack file."""
    pass