"""Async variation of espota"""
from asyncio import start_server, wait_for, StreamReader, Event
from typing import Callable
from .invitation import invite

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 11311
PACKET_SIZE = 1460

async def _check_status(reader: StreamReader):
    received_ok = False
    received_error = False
    while not (received_ok or received_error):
        reply = await reader.read(64)
        message = reply.decode("utf-8")
        if message.find('E') >= 0:
            received_error = True
        elif message.find('O') >= 0:
            received_ok = True
    return received_ok

async def update_ota(host: str, port: int, file: bytes, report: Callable) -> bool:
    """Sends espota invitation"""
    stop_request = Event()

    def next_chunk(offset) -> bytes:
        chunk_end = 0
        if offset+PACKET_SIZE <= len(file):
            chunk_end = offset+PACKET_SIZE
        elif offset < len(file):
            chunk_end = len(file)
        else:
            chunk_end = offset
        return file[offset:chunk_end]

    async def handle_connection(reader, writer):
        offset = 0
        while True:
            chunk = next_chunk(offset)
            offset += len(chunk)
            report(98 / (len(file) / offset))
            writer.write(chunk)
            await reader.read(32)
            if offset == len(file):
                report(99)
                success = await _check_status(reader)
                if not success:
                    raise Exception("Got error")
                stop_request.set()
                report(100)
                break

    server = await start_server(handle_connection, SERVER_HOST, SERVER_PORT)
    await wait_for(invite(host, port, SERVER_PORT, file), 1)
    await stop_request.wait()
    server.close()
