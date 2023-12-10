"""MyrtDesk transport types"""
from typing import List, Tuple

from typing_extensions import TypedDict

# Integer in range from 0 to 255
Byte = int

# List of bytes
Datagram = List[Byte]

# Socket domain message
SocketMessage = TypedDict('SocketMessage', {
    'domain': int,
    'command': int,
    'body': Datagram
})

# Socket address
Address = Tuple[str, int]
