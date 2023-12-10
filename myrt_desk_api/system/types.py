"""MyrtDesk system types"""
from enum import Enum

DOMAIN_SYSTEM = 0

class Command(Enum):
    """MyrtDesk system commands"""
    REBOOT = 1
    PING = 2
    READ_FREE_HEAP = 4
    BROADCAST_FREE_HEAP = 5
