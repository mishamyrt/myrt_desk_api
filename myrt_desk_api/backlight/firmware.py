"""MyrtDesk Backlight Firmware"""

from typing import List
from warnings import warn

PAGE_SIZE = 128

class FormatError(Exception):
    """Raised when the input format is not Intel HEX"""

class Firmware():
    """Converts Intel HEX formatted backlight firmware to AVRLord binary format"""

    _i: int = 0
    _page_i: int = 0
    _eof: bool = False
    _pages: List[List[int]] = []
    _page: List[int] = [0] * PAGE_SIZE
    _content: str = ''

    def __init__(self, content: str):
        self._content = content
        self._parse()
        self._content = ''

    @property
    def size(self):
        """Returns firmware bytes count"""
        return len(self._pages) * PAGE_SIZE

    @property
    def pages(self):
        """Returns firmware pages"""
        return self._pages

    def _parse(self):
        while not self._eof:
            if self._i >= len(self._content) - 1 or not self._read_line():
                raise FormatError
        if self._page_i != 0:
            self._fill_tail()
            page = self._page.copy()
            self._pages.append(page)

    def _read_line(self) -> bool:
        if self._content[self._i] != ":":
            warn(f"Wrong first symbol '{self._content[self._i]} at {self._i}'")
            return False
        self._i += 1
        length = self._read_byte() * 2
        if self._i + 7 + length > len(self._content) or length > PAGE_SIZE:
            warn("Wrong length")
            return False
        command_symbol = self._content[self._i + 5]
        if command_symbol == '0':
            self._i += 6
        elif command_symbol == '1':
            self._eof = True
            return True
        elif command_symbol == '4':
            # Skip line
            self._i += length + 9
            return True
        else:
            warn(f"Unknown command symbol '{command_symbol}'")
            return False
        self._read_body(length)
        self._i += 4
        return True

    def _read_body(self, length: int):
        end = self._i + length
        while self._i < end:
            self._page[self._page_i] = self._read_byte()
            self._page_i += 1
            if self._page_i == PAGE_SIZE:
                page = self._page.copy()
                self._pages.append(page)
                self._page_i = 0

    def _read_byte(self) -> int:
        first = self._content[self._i]
        second = self._content[self._i+1]
        self._i += 2
        return int(f"{first}{second}", 16)

    def _fill_tail(self):
        while self._page_i < PAGE_SIZE:
            self._page[self._page_i] = 0
            self._page_i += 1
