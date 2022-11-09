"""Tests discovery stability"""
from asyncio import run
from myrt_desk_api import discover

ATTEMPTS = 100

async def _main():
    success = 0
    count = 0
    while count < ATTEMPTS:
        result = await discover()
        is_avaliable = result is not None
        if is_avaliable:
            success += 1
        count += 1
        percent_progress = (count / ATTEMPTS) * 100
        percent_success = (count / success) * 100
        print(f"{percent_progress:.1f}% done, {percent_success:.1f}% successful", end="\r")
    print()

if __name__ == '__main__':
    run(_main())
