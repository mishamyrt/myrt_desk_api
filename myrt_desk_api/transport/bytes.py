"""MyrtDesk API transport byte utils"""

def low_byte(value: int) -> int:
    """Gets number low byte"""
    return value & 0xff

def high_byte(value: int) -> int:
    """Gets number high byte"""
    return value >> 8

def from_byte_pair(high: int, low: int) -> int:
    """Assembles a number from high and low bytes."""
    return (high << 8) + low
