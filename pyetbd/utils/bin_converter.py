import numpy as np
from numba import njit


@njit
def dec_to_bin(num, bits):
    binary = np.zeros(bits, dtype=np.int8)
    i = bits - 1
    while num > 0 and i >= 0:
        binary[i] = num % 2
        num //= 2
        i -= 1

    return binary


@njit
def bin_to_dec(binary):
    num = 0
    for i in range(len(binary)):
        num += binary[i] * 2 ** (len(binary) - i - 1)

    return num


@njit
def bit_flip(binary):
    bit = np.random.randint(0, len(binary))

    if binary[bit] == 0:
        binary[bit] = 1
    else:
        binary[bit] = 0

    return binary
