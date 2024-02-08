import os

from packaging.version import Version, parse, InvalidVersion


def save_bump(version_file_path, v: Version):
    with open(version_file_path, 'w') as version_file:
        version_file.write(f"__version__ = '{v}'\n")


def bump_version(v: Version, level='patch'):
    major = v.release[0]
    minor = v.release[1]
    patch = v.release[2]
    alpha = None if not v.pre else v.pre[1]
    dev = None if not v.is_devrelease else v.dev

    match level:
        case "major":
            major, minor, patch = major + 1, 0, 0
            alpha, dev = None, None
        case "minor":
            minor, patch = minor + 1, 0
            alpha, dev = None, None
        case "patch":
            patch += 1
            alpha, dev = None, None
        case "alpha":
            alpha = alpha + 1
            dev = None
        case "dev":
            dev = dev + 1

    version_str = f"{major}.{minor}.{patch}"
    if alpha is not None:
        version_str += f"a{alpha}"
    if dev is not None:
        version_str += f"dev{dev}"
    return parse(version_str)


def parse_version(source_folder, module_name) -> Version:
    version_file_path = os.path.join(source_folder, module_name, "__version__.py")

    try:
        with open(version_file_path, 'r') as version_file:
            version_globals = {}
            exec(version_file.read(), version_globals)
            raw_version = version_globals.get('__version__')

            if raw_version:
                try:
                    # Validate the version using the packaging library
                    return parse(raw_version)
                except InvalidVersion:
                    print(f"Warning: Invalid version '{raw_version}' in '{module_name}'.")

            else:
                raise ValueError(f"No version found in '{module_name}'.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Version file not found for '{module_name}'.")
