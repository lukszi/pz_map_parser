from pathlib import Path
from zomboid_map_parser.processing import Parser

# Initialize the parser with your game directory
parser = Parser(Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\ProjectZomboid\\media"))

# Parse everything
parser.parse_all()

# Get statistics
stats = parser.get_statistics()
print(f"Parsed {stats['map_cells']} cells with {stats['total_tiles']} total tiles")