"""System CLI commands"""
from datetime import datetime
from ... import MyrtDesk
from ..progress import print_progress

__all__ = ['system_commands']

async def handle_reboot(_, desk: MyrtDesk):
    """Handles a reboot command"""
    await desk.system.reboot()

async def handle_logs(_, desk: MyrtDesk):
    """Handles a logs command"""
    def handle_log_line(message: str):
        print(f"{datetime.now()}: [Desk]: {message}")
    print("Listening for logs from desk")
    await desk.system.read_logs(handle_log_line)

async def handle_flash(args, desk: MyrtDesk):
    """Handles a flash-controller command"""
    print("Updating desk's legs firmware...")
    with open(args.path, mode="rb") as file:
        contents = file.read()
        await desk.system.update_firmware(contents, print_progress)

async def handle_heap(_, desk: MyrtDesk):
    """Handles a heap command"""
    free = await desk.system.read_heap()
    print(f"Free heap: {free} bytes")

def system_commands(subparser):
    """Appends system commands"""
    # A reboot command
    subparser.add_parser('reboot', help='Reboot MyrtDesk system')
    # A logs command
    subparser.add_parser('logs', help='Reads logs from device')
    # A flash-controller command
    flash_controller_parser = subparser.add_parser('flash-controller',
        help='Update desk\'s controller firmware')
    flash_controller_parser.add_argument('path',
        action='store', help='The path to the firmware to be installed')
    # A heap command
    subparser.add_parser('heap', help='Reads device free heap')
    return [
        ('reboot', handle_reboot),
        ('logs', handle_logs),
        ('flash-controller', handle_flash),
        ('heap', handle_heap),
    ]
