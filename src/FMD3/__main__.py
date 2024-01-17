from FMD3.Core import load_extensions, download
from FMD3.Core.hello import hello
from FMD3.Extensions import extesion_factory, get_extension

#
# for extension in extesion_factory:
#     extension.print_ext_name()fr
from FMD3.Core.logging import setup_logging, TRACE

setup_logging("config/log.log",TRACE)
load_extensions()
ext = get_extension("MangaDex")
# download([
#     (ext,["a508faf3-b175-43b8-88e7-7e7231290892"])
# ]
# )

for extension in extesion_factory:
    extension.print_ext_name()