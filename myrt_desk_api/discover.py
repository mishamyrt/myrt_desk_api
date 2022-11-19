"""MyrtDesk discovery helper"""
from typing import Union
from asyncio import exceptions, wait_for, sleep
from socket import getfqdn, gethostname, gethostbyname_ex
from .datagram import open_broadcast, open_endpoint, Endpoint
from .system.constants import DOMAIN_SYSTEM, COMMAND_PING
from .constants import API_PORT

__all__=['discover', 'is_desk']

PING_REQUEST = bytes([
    2,
    DOMAIN_SYSTEM,
    COMMAND_PING
])

def apply_mask(local_address: str, mask: str) -> str:
    """Applies the netmask to the /24 address"""
    segments = local_address.split(".")
    mask_segments = mask.split(".")
    result_address = ""
    index = 0
    for segment in mask_segments:
        if len(result_address) > 0:
            result_address += "."
        if segment == "255":
            result_address += f"{segments[index]}"
        elif segment == "0":
            result_address += "255"
        index += 1
    return result_address

def get_discovery_host() -> str:
    """Finds discovery host"""
    hosts = gethostbyname_ex(getfqdn(gethostname()))
    local_ips = hosts[2]
    if len(local_ips) > 1:
        return ""
    return apply_mask(local_ips[0], "255.255.255.0")

async def discover(host: str = None) -> Union[None, str]:
    """Finds desk IP address on network via broadcast ping"""
    if host is None:
        host = '255.255.255.255'
    broadcast = await open_broadcast((host, API_PORT))
    attempts = 5
    while attempts != 0:
        try:
            broadcast.send(PING_REQUEST)
            item = await broadcast.receive(1.0, 1)
            response_data = list(item[0][0])
            if len(response_data) == response_data[0] + 1 and response_data[3] == 0:
                return item[0][1][0]
        except (exceptions.TimeoutError, IndexError):
            attempts -= 1
    return None

async def is_desk(host: str, attempts: int = 2) -> bool:
    """Checks if host is MyrtDesk"""
    endpoint: Endpoint = None
    async def close():
        if endpoint is not None:
            endpoint.close()
            await sleep(0.1)
    while attempts != 0:
        try:
            endpoint = await open_endpoint(host, API_PORT)
            endpoint.send(PING_REQUEST)
            await wait_for(endpoint.receive(), 0.25)
            await close()
            return True
        except exceptions.TimeoutError:
            await close()
            attempts -= 1
    return False
