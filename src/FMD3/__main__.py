from FMD3.Core.hello import hello
from FMD3.Extensions import extesion_factory

hello()


for extension in extesion_factory:
    extension.print_ext_name()