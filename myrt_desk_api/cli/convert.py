def hex_to_rgb(val):
    return tuple(int(val[i : i + 2], 16) for i in (0, 2, 4))
