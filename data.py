import json
import os

_cache = {}

def file_exists(name):
    try:
        os.stat(name)
        return True
    except OSError:
        return False

def __getattr__(name):
    """
    Called when someone tries to import a name that doesn't exist 
    in this module. We'll check if a matching .json file exists.
    """
    if name in _cache:
        return _cache[name]

    # Construct the expected filename: data_files/name.json
    file_path = f"/data_files/{name}.json"

    if file_exists(file_path):
        with open(file_path, 'r') as f:
            # Load the data and cache it
            data = json.load(f)
            _cache[name] = data
            return data

    raise AttributeError(f"No JSON file found for '{name}' at {file_path}")
