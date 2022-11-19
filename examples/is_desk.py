"""Tests discovery stability"""
from asyncio import run
from myrt_desk_api.discover import is_desk

async def _main():
    test_hosts = ['192.168.31.16', '192.168.31.222', '192.168.31.37']
    for host in test_hosts:
        verb = "is" if await is_desk(host) else "is not"
        print(f"{host} {verb} the MyrtDesk")

if __name__ == '__main__':
    run(_main())
