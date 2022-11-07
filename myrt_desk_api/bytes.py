"""Bytes helpers"""

def low_byte(value: int):
    """Gets number low byte"""
    return value & 0xff

def high_byte(value: int):
    """Gets number low byte"""
    return value >> 8
