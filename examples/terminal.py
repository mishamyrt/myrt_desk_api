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
    print("UDP socket stream command terminal")
    stream = SocketStream('MyrtDesk.local')

    async def listen_messages():
        async for message in stream.messages():
            print("Message:", message)
    asyncio.create_task(listen_messages())

    print("Connecting...")
    await stream.connect()
    print("Stream is connected. Enter commands to execute. Enter 0 to exit")
    while True:
        command = await read_command()
        if len(command) == 1 and command[0] == 0:
            print("Exiting...")
            await stream.close()
            return
        if command is None:
            print("Wrong command format.")
            print("It should be a list of numbers separated by a space. For example: 3 13 1")
            continue
        success = await stream.send(command)
        print("Status: " + "success" if success else "error")

if __name__ == '__main__':
    asyncio.run(main())
