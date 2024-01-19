import os

from setuptools import setup

excludes = [
    "TestExt"
]

def find_extensions():
    modules = []
    for module in next(os.walk("src/FMD3_Sources"))[1]:
        if module in excludes:
            continue

        print(f"Creating entrypoint for {module}")
        module_entry_point = f"FMD3_Sources.{module}=FMD3_Sources.{module}.{module}:load_source"

        modules.append(module_entry_point)

    return {"FMD3_Sources": modules}

setup(
    entry_points = find_extensions()
)