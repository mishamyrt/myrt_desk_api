"""Legs CLI commands"""
from arrrgs import command, arg
from ... import MyrtDesk

@command(
    arg('--set', required=False, default=None, type=int,
        help='Set new height in millimeters', dest="height")
)
async def height(args, desk: MyrtDesk):
    """Controlls desk's height"""
    if args.height is None:
        current_height = await desk.legs.get_height()
        print(f"Current height is {current_height} mm.")
    else:
        await desk.legs.set_height(args.height)

@command()
async def calibrate(_, desk: MyrtDesk):
    """Calibrates desk's height sensor"""
    await desk.legs.caibrate()
    print('Calibration is started')
