import re
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SocketType
from typing import Tuple, Dict, Callable, AnyStr, List


class CommandParser:
    patterns: List = [
        r'(?P<command>ADD) (?P<queue>\S+) (?P<length>\d{1,9}) (?P<data>.+)',
        r'(?P<command>GET) (?P<queue>\S+)',
        r'(?P<command>ACK) (?P<queue>\S+) (?P<id>.+)',
        r'(?P<command>IN) (?P<queue>\S+) (?P<id>.+)',
        r'(?P<command>SAVE)'
    ]

    def __init__(self, command: str):
        self.command: AnyStr = command
        self._compiled_patterns: List = []
        for pattern in self.patterns:
            self._compiled_patterns.append(re.compile(bytes(pattern, 'utf8')))
    
    def get_command_match(self) -> Dict:
        for pattern in self._compiled_patterns:
            if match := pattern.match(self.command):
                return match.groupdict()


class SocketServer:
    
    BUFFER_SIZE = 1024

    def __init__(self, ip: str, port: int):
        self._ip: str = ip
        self._port: int = port
        self._sock: SocketType = socket(AF_INET, SOCK_STREAM)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._sock.bind((self._ip, self._port))
        self._sock.listen(1)

    def run(self, callback: Callable) -> None:
        while True:
            conn, addr = self._sock.accept()
            self._handle_connection(conn, addr, callback)

    def _handle_connection(self, connection: SocketType, address: Tuple, callback: Callable) -> None:
        with connection:
            data = connection.recv(self.BUFFER_SIZE)
            task = CommandParser(data).get_command_match()
            if not task:
                connection.send(b'ERROR')
            else:
                response = callback(task)
                connection.send(response)
