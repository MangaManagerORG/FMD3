import FMD3.Extensions
from FMD3.Extensions import IExtension


def do_something():
    print("not somethig")


def test():
    print("extension run")
    return "Ok"


class TestExt(IExtension):
    def print_ext_name(self):
        print(f"My Extension name isssssss: {self.extension_name}")

    ...


def load_extension():
    FMD3.Extensions.add_Extension(TestExt())
