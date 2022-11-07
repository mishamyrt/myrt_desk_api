"""Invitation espota helpers"""
from hashlib import md5
from ..datagram import open_endpoint

COMMAND_FLASH = 0

def _format_invitation(port: int, file: bytes):
    return f"{COMMAND_FLASH} {port} {len(file)} {md5(file).hexdigest()}\n"

async def invite(host: str, port: int, local_port: int, file: bytes) -> None:
    """Invite espota client"""
    message = _format_invitation(local_port, file)
    endpoint = await open_endpoint(host, port)
    endpoint.send(message.encode())
    await endpoint.receive()
