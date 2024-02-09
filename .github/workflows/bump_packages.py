import os

from promidius_versioning_utils import bump_packages_if_modified

if __name__ == '__main__':
    src_path = 'src'
    packages = ['FMD3', 'FMD3_API', 'FMD3_Tkinter']
    bump_level = os.getenv('BUMP_LEVEL', 'patch')
    bump_packages_if_modified(src_folder=src_path, packages=packages, bump_level=bump_level)
