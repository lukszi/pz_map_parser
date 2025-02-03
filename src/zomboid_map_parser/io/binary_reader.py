# io/binary_reader.py
import struct
from pathlib import Path
from typing import BinaryIO

class BinaryReader:
    """
    Handles reading binary data with configurable byte order handling.

    The reader supports both big-endian and little-endian formats. Big-endian
    matches the original C# implementation's behavior, while little-endian
    support has been added for compatibility with other file formats.
    """

    def __init__(self, file: BinaryIO):
        """
        Initialize the binary reader.

        Args:
            file: The binary file to read from
        """
        self.file = file
        self.bytes_read = 0

    def get_name(self) -> str:
        file_name: str = "unknown"
        if self.file.name:
            file_path = Path(self.file.name)
            file_name = file_path.stem
        return file_name

    def read_byte(self) -> int:
        """
        Read a single byte.
        Note: Single bytes are not affected by endianness.
        """
        self.bytes_read += 1
        data = self.file.read(1)
        return int.from_bytes(data)

    def read_int16(self, big_endian: bool = True) -> int:
        """Read a 16-bit integer with configured endianness."""
        self.bytes_read += 2
        data = self.file.read(2)
        fmt = '>' if big_endian else '<'
        return struct.unpack(f'{fmt}h', data)[0]

    def read_int32(self, big_endian: bool = True) -> int:
        """Read a 32-bit integer with configured endianness."""
        self.bytes_read += 4
        data = self.file.read(4)
        fmt = '>' if big_endian else '<'
        return struct.unpack(f'{fmt}i', data)[0]

    def read_int64(self, big_endian: bool = True) -> int:
        """Read a 64-bit integer with configured endianness."""
        self.bytes_read += 8
        data = self.file.read(8)
        fmt = '>' if big_endian else '<'
        return struct.unpack(f'{fmt}q', data)[0]

    def read_single(self, big_endian: bool = True) -> float:
        """Read a 32-bit float with configured endianness."""
        self.bytes_read += 4
        data = self.file.read(4)
        fmt = '>' if big_endian else '<'
        return struct.unpack(f'{fmt}f', data)[0]

    def read_double(self, big_endian: bool = True) -> float:
        """Read a 64-bit float with configured endianness."""
        self.bytes_read += 8
        data = self.file.read(8)
        fmt = '>' if big_endian else '<'
        return struct.unpack(f'{fmt}d', data)[0]

    def read_string(self) -> str:
        """
        Read a string until newline character.
        Note: String reading is not affected by endianness.
        """
        result = []
        while True:
            char = self.file.read(1).decode('utf-8')
            self.bytes_read += 1
            if char == '\n':
                break
            result.append(char)
        return ''.join(result)

    def read_bytes(self, count: int) -> bytes:
        """
        Read specified number of bytes.
        Note: Raw byte reading is not affected by endianness.
        """
        self.bytes_read += count
        return self.file.read(count)

    def peek_byte(self) -> int:
        """
        Look at the next byte without advancing the read position.
        Useful for checking what's coming next in the stream.
        """
        pos = self.file.tell()
        value = self.read_byte()
        self.file.seek(pos)
        self.bytes_read -= 1  # Undo the byte count since we moved back
        return value