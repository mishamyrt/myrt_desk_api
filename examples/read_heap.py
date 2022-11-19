"""Tests discovery stability"""
from asyncio import run, sleep
from myrt_desk_api import discover, MyrtDesk

ATTEMPTS = 100

async def _main():
    host = await discover()
    if host is None:
        exit(1)
    desk = MyrtDesk(host)
    while True:
        result = await desk.system.read_heap()
        print(result)
        await sleep(0.5)

if __name__ == '__main__':
    run(_main())