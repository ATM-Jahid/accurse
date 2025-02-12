import sys
from accurse.toml_util import read_toml

def main() -> bool:
    # Provide path to the TOML file
    metadata_path = sys.argv[1]
    read_toml(metadata_path)

    return True
