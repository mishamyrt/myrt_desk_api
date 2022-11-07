from asyncio import run
from myrt_desk_api import MyrtDesk

async def main():
    """Example entrypoint"""
    # await discover()
    # desk = MyrtDesk('192.168.31.16')

    # await desk.backlight.set_brightness(100)
    # await desk.backlight.set_color((0, 0, 255))
    # await desk.legs.set_height(1100)

if __name__ == '__main__':
    run(main())
