"""MyrtDesk transport ping utils"""
from os import system


def ping(host: str, timeout = 1):
    """Pings host availability"""
    response = system(f"ping -c 1 -t {timeout} {host} 2>&1 >/dev/null")
    return response == 0
