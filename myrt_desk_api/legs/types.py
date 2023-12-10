"""MyrtDesk legs constants"""
from enum import Enum

DOMAIN_LEGS = 2

class Command(Enum):
    """MyrtDesk legs commands"""
    READ_HEIGHT = 0
    SET_HEIGHT = 1
    CALIBRATE = 3
    BROADCAST_STATE = 4
