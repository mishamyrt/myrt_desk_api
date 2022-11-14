"""Backlight CLI commands"""
from ... import MyrtDesk
from ..assert_val import assert_byte
from ..progress import print_progress

__all__ = ['backlight_commands']

async def handle_color(args, desk: MyrtDesk):
    """Handles a color command"""
    hex_color = args.hex_color
    if len(hex_color) == 7:
        hex_color = hex_color[1:]
    color = _hex_to_rgb(hex_color)
    await desk.backlight.set_color(color)

async def handle_white(args, desk: MyrtDesk):
    """Handles a white command"""
    assert_byte(args.warmness)
    await desk.backlight.set_white(args.warmness)

async def handle_effect(args, desk: MyrtDesk):
    """Handles an effect command"""
    await desk.backlight.set_effect(args.effect)

async def handle_flash(args, desk: MyrtDesk):
    """Handles a backlight-flash command"""
    print("Updating desk's backlight firmware...")
    with open(args.path, mode="rb") as file:
        contents = file.read()
        await desk.backlight.update_firmware(contents, print_progress)

async def handle_on(_, desk: MyrtDesk):
    """Handles an power on command"""
    await desk.backlight.set_power(True)

async def handle_off(_, desk: MyrtDesk):
    """Handles an power off command"""
    await desk.backlight.set_power(False)

def backlight_commands(subparser):
    """Appends backlight commands"""
    # A color command
    color_parser = subparser.add_parser('color', help='Set backlight color')
    color_parser.add_argument('hex_color', help='Hexadecimal color value')
    # A white command
    white_parser = subparser.add_parser('white', help='Set backlight color')
    white_parser.add_argument('warmness', help='0-255 warmness level', type=int)
    # An effect command
    effect_parser = subparser.add_parser('effect', help='Set backlight effect')
    effect_parser.add_argument('effect', help='Effect index', type=int)
    # A flash-backlight command
    firmware_parser = subparser.add_parser('flash-backlight',
        help='Update desk\'s backlight firmware')
    firmware_parser.add_argument('path', action='store', help='The path to the Intel HEX firmware')
    # A power commands
    subparser.add_parser('on', help='Enables backlight')
    subparser.add_parser('off', help='Disables backlight')
    return [
        ('color', handle_color),
        ('white', handle_white),
        ('effect', handle_effect),
        ('flash-backlight', handle_flash),
        ('on', handle_on),
        ('off', handle_off)
    ]

def _hex_to_rgb(val):
    return tuple(int(val[i : i + 2], 16) for i in (0, 2, 4))
