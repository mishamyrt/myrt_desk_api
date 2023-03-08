"""Invitation espota helpers"""
from hashlib import md5

from asyncio_dgram import connect

COMMAND_FLASH = 0

def _format_invitation(port: int, file: bytes):
    return f"{COMMAND_FLASH} {port} {len(file)} {md5(file).hexdigest()}\n"

async def invite(host: str, port: int, local_port: int, file: bytes) -> None:
    """Invite ESPota client"""
    message = _format_invitation(local_port, file)
    stream = await connect((host, port))
    await stream.send(message.encode())
    await stream.recv()
