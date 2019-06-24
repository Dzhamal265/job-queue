from .socketserver import SocketServer
from .taskqueue import TaskQueue
from typing import Dict


class TaskQueueServer:
    def __init__(self, ip: str, port: int, path: str, timeout: int):
        self._server: SocketServer = SocketServer(ip, port)
        self._task_queue: TaskQueue = TaskQueue(path, timeout)

    def run(self) -> None:
        return self._server.run(self._dispatch)

    def _add(self, command: bytes, *args: Dict) -> bytes:
       return self._task_queue.add(*args)

    def _get(self, command: bytes, *args: Dict) -> bytes:
        return self._task_queue.get(*args)

    def _ack(self, command: bytes, *args: Dict) -> bytes:
        return self._task_queue.ack(*args)

    def _inq(self, command: bytes, *args: Dict) -> bytes:
        return self._task_queue.inq(*args)

    def _save(self, *args: Dict) -> bytes:
        return self._task_queue.save(*args)

    @staticmethod
    def from_bytes_to_str(task: bytes) -> str:
        return task.lower().decode('utf-8')

    def _dispatch(self, task: Dict) -> bytes:
        command = task['command'] # cache result
        task = task.values()
        
        if self.from_bytes_to_str(command) == 'in':
            name = f'_{self.from_bytes_to_str(command)}q'
        else:
            name = f'_{self.from_bytes_to_str(command)}'

        return getattr(self, name)(*task)
