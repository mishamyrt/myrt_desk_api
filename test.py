import asyncio
from myrt_desk_api import MyrtDesk

async def main():
    """Shut up"""
    # desk_host = await discover()
    desk = MyrtDesk("MyrtDesk.local")
    await asyncio.gather(
        desk.backlight.set_power(True),
        desk.backlight.set_color((0, 255, 0)),
        desk.backlight.set_brightness(50)
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main()))
