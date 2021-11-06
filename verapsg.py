"""
Python interface to the vera psg emulator code from X16Emu
"""

from _verapsg import lib, ffi
import array


__version__ = "1.0"


def freqw(hz: int) -> int:
    return int(hz / (48828.125 / 2**17))


def reset() -> None:
    lib.psg_reset()


def writereg(reg: int, value: int) -> None:
    lib.psg_writereg(reg, value)


def render(num_samples: int) -> bytearray:
    buffer = bytearray(num_samples*4)
    lib.psg_render(ffi.from_buffer("int16_t *", buffer), num_samples)
    return buffer


def render_a(num_samples: int) -> array.array:
    buffer = array.array('h', [0]*num_samples*2)
    lib.psg_render(ffi.from_buffer("int16_t *", buffer, True), num_samples)
    return buffer


reset()
