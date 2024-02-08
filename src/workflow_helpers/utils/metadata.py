import json
sources_file_path = "versions_metadata.json"

def load_version_metadata():
    try:
        with open(sources_file_path, 'r') as sources_file:
            return json.load(sources_file)
    except FileNotFoundError:
        return {}


def save_version_metadata(data):
    with open(sources_file_path, 'w') as sources_file:
        json.dump(data, sources_file, indent=2)


