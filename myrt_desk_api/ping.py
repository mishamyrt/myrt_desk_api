"""Ping utilities"""
from os import system
from asyncio import sleep

def ping(host: str, timeout = 1):
    """Pings host avalibility"""
    response = system(f"ping -c 1 -t {timeout} {host} 2>&1 >/dev/null")
    return response == 0

async def host_down(host: str, inteval = 0.5):
    """Waits for host to be unavaliable"""
    while True:
        if not ping(host):
            return
        await sleep(inteval)

async def host_up(host: str, inteval = 0.5):
    """Waits for host to be unavaliable"""
    while True:
        if ping(host):
            return
        await sleep(inteval)
