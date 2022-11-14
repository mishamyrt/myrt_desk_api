"""Assert helpers"""

def assert_byte(val: int) -> None:
    """Asserts value to be in 0—255 range"""
    if val > 255 or val < 0:
        raise Exception("Wrong byte value")
