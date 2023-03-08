"""MyrtDesk CLI module"""
from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import Callable, Dict, List, Tuple
from logging import getLogger, DEBUG
from .. import MyrtDesk
from ..discover import discover

CommandHandler = Callable[[Namespace, MyrtDesk], None]
CommandsRegistrar = Callable[[_SubParsersAction], List[Tuple[str, CommandHandler]]]

_LOG = getLogger(__file__)

class MyrtDeskCLI:
    """MyrtDesk CLI controller"""
    _parser: ArgumentParser = None
    _command_parser = None
    _handlers: Dict = {}
    _args: Namespace

    def __init__(self):
        self._parser = ArgumentParser()
        self._parser.add_argument('--debug',
            default=False,
            action='store_true',
            help='Increases the amount of information the script prints')
        self._parser.add_argument('--host', '-d',
            default=None,
            action='store_true',
            dest='host',
            help='MyrtDesk host address')
        self._command_parser = self._parser.add_subparsers(help='List of commands', dest="command")
        self._command_parser.default = None

    def register(self, *args: List[CommandsRegistrar]) -> None:
        """Adds command handlers"""
        for registrar in args:
            commands = registrar(self._command_parser)
            for (command, handler) in commands:
                self._handlers[command] = handler

    async def run(self):
        """App entrypoint"""
        self._args = self._parser.parse_args()
        if self._args.debug:
            _LOG.setLevel(DEBUG)
        host = ''
        if self._args.host is not None:
            host = self._args.host
        else:
            host = await discover()
        desk = MyrtDesk(host)
        if self._args.command not in self._handlers:
            print('Unknown command')
        await self._handlers[self._args.command](self._args, desk)
