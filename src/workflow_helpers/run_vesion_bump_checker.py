import os
from pathlib import Path
from typing import Literal
from utils.metadata import load_version_metadata, save_version_metadata
from utils.version import bump_version, parse_version, save_bump
from utils.git import has_code_changed


def check_and_bump_modules(src_folder, excluded=None,
                           bump_level: Literal["major", "minor", "patch", "alpha", "dev"] = 'patch'):
    packages_version_metadata = load_version_metadata()

    if excluded is None:
        excluded = list()
    for module_name in os.listdir(src_folder):
        if any([excluded_module in module_name for excluded_module in excluded]):
            print(f"Skipping {module_name}")
            continue
        print(f"Checking and bumping {module_name}")

        module_has_update = has_code_changed(src_folder, module_name, packages_version_metadata)
        if module_has_update:
            version = parse_version(src_folder, module_name)
            print(f"Current version: {version}")
            bumped_version = bump_version(version, bump_level)
            print(f"Bumped version: {bumped_version}")
            packages_version_metadata[module_name] = {
                "version": str(bumped_version),
                "commit_hash": module_has_update
            }
            print("Bumping version...")
            save_bump(os.path.join(src_folder, module_name, "__version__.py"), bumped_version)
            print(f"Version successfully bumped to {bumped_version} for package {module_name}")
        else:
            print(f"No changes detected in package '{module_name}'.")
    print("Saving metadata")
    print(packages_version_metadata)

    save_version_metadata(packages_version_metadata)

if __name__ == '__main__':
    excluded = ["egg-info","workflow_helpers"]
    check_and_bump_modules(Path(__file__).parent.parent, excluded=excluded, bump_level='patch')