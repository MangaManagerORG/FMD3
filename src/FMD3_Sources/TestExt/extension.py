from FMD3.Sources.ISource import ISource


def do_something():
    print("not something")


def test():
    print("extension run")
    return "Ok"


class TestExt(ISource):
    def print_ext_name(self):
        print(f"My Extension name isssssss: {self.extension_name}")

    ...


def load_extension():
    FMD3.Sources.add_source(TestExt())
