"""
Python interface to the vera psg emulator code from x16emu
This module uses CFFI to create the glue code but also to actually compile everything else too!
"""


import os
from cffi import FFI


ffibuilder = FFI()
ffibuilder.cdef("""

void psg_reset(void);
void psg_writereg(uint8_t reg, uint8_t val);
void psg_render(int16_t *buf, unsigned num_samples);

""")


libraries = []
compiler_args = []
macros =  []

if os.name == "posix":
    libraries = []  # ["m", "pthread", "dl"]
    compiler_args = ["-g1", "-O3"]
    macros.extend([
        ("HAVE_LIBM", "1"),
        ("HAVE_UNISTD_H", "1"),
    ])


custom_sources = []
verapsg_sources = ["vera_psg.c"]


ffibuilder.set_source("_verapsg", """
  
#include <stdint.h>

void psg_reset(void);
void psg_writereg(uint8_t reg, uint8_t val);
void psg_render(int16_t *buf, unsigned num_samples);

""",
    sources=custom_sources + verapsg_sources,
    include_dirs=[],
    libraries=libraries,
    define_macros=macros,
    extra_compile_args=compiler_args)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
