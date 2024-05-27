"""Generates the CFFI bindings for the tb_client library."""

import cffi
from pathlib import Path

this_dir = Path().absolute()
lib_dir = this_dir.parent.joinpath("c", "lib", "x86_64-linux-gnu")
h_file = this_dir.joinpath("tb_client", "native", "tb_client.h")

ffi = cffi.FFI()

with h_file.open() as c_header:
    c_header = c_header.read()

defs = f"""\
{c_header}

extern "Python" void on_completion_fn(uintptr_t, tb_client_t, tb_packet_t*, const uint8_t*, uint32_t);
"""

ffi.cdef(
    # f'{c_header}\n\nextern "Python" void on_completion_fn(uintptr_t, tb_client_t, tb_packet_t*, const uint8_t*, uint32_t);\n'
    defs
)

head = """\
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include "native/tb_client.h"
"""

ffi.set_source(
    "tb_client._tb_client",
    head,
    libraries=["tb_client"],
    library_dirs=[lib_dir.as_posix()],
    # library_dirs=["tb_client/native/x86_64-linux-gnu.2.27/"],
    # library_dirs=[this_dir.as_posix()],
    extra_link_args=[f"-Wl,-rpath,{lib_dir.as_posix()}"],
)

if __name__ == "__main__":
    ffi.compile(verbose=True)
