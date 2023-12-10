"""Tests discovery stability"""
from __future__ import annotations

import asyncio
from typing import List

from aioconsole import ainput

from myrt_desk_api.transport import SocketStream


def parse_numbers(input_string) -> List[int] | None:
    try:
        split_values = input_string.split()
        numbers = [int(value) for value in split_values]
        return numbers
    except ValueError as e:
        print(e)
        return None

async def read_command() -> List[int] | None:
    user_input = await ainput("Command: ")
    return parse_numbers(user_input)

async def main():
    loop = asyncio.get_event_loop()
    print("UDP socket stream command terminal")
    desk_addr = ("MyrtDesk.local", 11011)
    stream = SocketStream(desk_addr, loop)

    async def listen_messages():
        async for message in stream.messages():
            print("Message:", message)

    print("Connecting...")
    await stream.connect()
    task = loop.create_task(listen_messages())
    print(f"Stream is connected on {stream.port}. Enter commands to execute. Enter 0 to exit")
    while True:
        await asyncio.sleep(10)
        success = await stream.send([1, 0])
        print("Status: " + ("success" if success else "error"))
    await stream.close()
    task.cancel()
if __name__ == '__main__':
    asyncio.run(main())

# command = await read_command()
# if len(command) == 1 and command[0] == 0:
#     print("Exiting...")
#     await stream.close()
#     return
# if command is None:
#     print("Wrong command format.")
#     print("It should be a list of numbers separated by a space. For example: 3 13 1")
#     continue