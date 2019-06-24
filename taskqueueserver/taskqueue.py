from collections import deque
from typing import Deque, Dict
from uuid import uuid4
from time import time
import pickle 
from os.path import abspath, join, exists

class TaskQueue:
    def __init__(self, path: str, timeout: int):
        self._queue: Dict = {}
        self._path: str = join('./', 'checkpoint/')
        self._timeout: int = timeout
        self._processing_tasks: Dict = {}
        self._restore_queues()
        

    def __str__(self) -> Dict:
        return self._queue
    
    def _restore_queues(self) -> None:
        try:
            pickle_file = open(self._path + 'store.pickle', 'rb')
            queue, processing_tasks = pickle.load(pickle_file)
        except FileNotFoundError:
            print(f'No store.pickle file found in "{self._path}".')
        except EOFError:
            print(f'File "{self._path}/store.pickle empty.')
        else:
            pickle_file.close()
            self._queue = queue
            self._processing_tasks = processing_tasks

    # for ready queue
    def add(self, queue: bytes, length: bytes, data: bytes) -> bytes:
        task_id = bytes(str(uuid4()), 'utf8')
        if queue not in self._queue:
            self._queue[queue] = deque()
        self._queue[queue].append({
            'id': task_id,
            'length': length,
            'data': data
        })
        return task_id
        
    # for proccessing queue
    def _process_task(self, queue: bytes, task_id: bytes) -> None:
        if queue not in self._processing_tasks:
            self._processing_tasks[queue] = deque()
        self._processing_tasks[queue].append({
            'queue': queue,
            'id': task_id 
        })

    def get(self, queue: bytes) -> bytes:
        if queue not in self._queue:
            return b'NONE'
        task_id, length, data = self._queue[queue].popleft().values()
        self._process_task(queue, task_id)
        return b' '.join((task_id, length, data))

    def ack(self, queue: bytes, id: bytes) -> bytes: 
        if self._processing_tasks[queue]:
            self._processing_tasks[queue].popleft() 
            return b'YES'
        return b'NO'

    def inq(self, queue: bytes, id: bytes) -> bytes:
        queue_list = list(
            list(self._queue.get(queue, [])) + 
            list(self._processing_tasks.get(queue, []))
        )
        for task in queue_list: 
            if task['id'] == id:
                return b'YES'
        return b'NO'
    
    def save(self, command: bytes)  -> bytes:
        path = join(self._path,'store.pickle')
        with open(path, 'wb') as pickle_file:
            obj_tuple = (self._queue, self._processing_tasks)
            pickle.dump(obj_tuple, pickle_file)
        return b'SAVED'