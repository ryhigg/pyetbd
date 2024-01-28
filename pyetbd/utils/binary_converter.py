import numpy as np
from numba import njit


@njit
def dec_to_bin(num: int, bits: int) -> np.ndarray:
    binary = np.zeros(bits, dtype=np.int8)
    i = bits - 1
    while num > 0 and i >= 0:
        binary[i] = num % 2
        num //= 2
        i -= 1

    return binary


@njit
def bin_to_dec(binary: np.ndarray) -> int:
    num = 0
    for i in range(len(binary)):
        num += binary[i] * 2 ** (len(binary) - i - 1)

    return num


@njit
def bit_flip(binary: np.ndarray) -> np.ndarray:
    bit = np.random.randint(0, len(binary))

    if binary[bit] == 0:
        binary[bit] = 1
    else:
        binary[bit] = 0

    return binary


@njit
def convert_binary_to_decimal(binaries: np.ndarray) -> np.ndarray:
    """Converts an array of binary numbers to an array of decimal numbers.

    Args:
        binaries (np.ndarray): an array of binaries

    Returns:
        np.ndarray: an array of decimal numbers
    """
    decimals = np.empty(len(binaries), dtype=np.int64)
    for i in range(len(binaries)):
        decimals[i] = bin_to_dec(binaries[i])

    return decimals
