import abc

from FMD3.Extensions.IExtension import IExtension


def do_something():
    print("sdasdsadsdas")

extesion_factory:list[IExtension] = []

@abc.abstractmethod
def load_extension(extension: IExtension):
    ...
def add_Extension(extension:IExtension):
    extesion_factory.append(extension)
