"""Legs CLI commands"""
from ... import MyrtDesk

__all__ = ['legs_commands']

async def handle_height(args, desk: MyrtDesk):
    """Handles a height commands"""
    if args.height is None:
        height = await desk.legs.get_height()
        print(f"Current height is {height} mm.")
    else:
        await desk.legs.set_height(args.height)

async def handle_calibrate(_, desk: MyrtDesk):
    """Handles a calibrate command"""
    await desk.legs.caibrate()
    print('Calibration is started')

def legs_commands(subparser):
    """Appends system commands"""
    # A height commands
    height_parser = subparser.add_parser('height', help='Read desk\'s height')
    height_parser.add_argument('--set',
        required=False, default=None, type=int,
        help='Set new height in millimeters', dest="height"
    )
    # A calibrate command
    subparser.add_parser('calibrate', help='Calibrate desk height')
    return [
        ('height', handle_height),
        ('calibrate', handle_calibrate)
    ]
