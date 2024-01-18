from importlib.metadata import entry_points


def load_sources():
    display_eps = entry_points(group='FMD3_Extensions')
    for entry in display_eps:
        if entry.attr == "load_extension":
            module = entry.load()
            print(module)
            module()


