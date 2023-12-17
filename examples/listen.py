"""Tests discovery stability"""
from __future__ import annotations

import asyncio
from typing import List

from aioconsole import ainput

from myrt_desk_api import MyrtDesk

async def main():
    loop = asyncio.get_event_loop()
    desk = MyrtDesk("MyrtDesk.local", loop=loop)
    await desk.connect()
    await desk.backlight.read_state()
    # await asyncio.sleep(5)
    await desk.close()

if __name__ == '__main__':
    asyncio.run(main())
