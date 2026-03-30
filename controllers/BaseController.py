from abc import ABC, abstractmethod
import asyncio
from typing import Optional, List
import threading
from collections import deque

# 控制器状态机
class ControllerStatus:
    Disconnected = 0
    Init = 1
    Ready = 2
    Running = 3
    Stopped = 4
    Error = 5
    Exit = 6



# 继承ABC类
class BaseController(ABC):
    
    def __init__(self, ws_url:str, local_port:int=0, enable_kcp:bool=False, crl_hz:int=500, device_id:int=0):
        self._async_loop = None
        self._ws_url = ws_url
        self._local_port = local_port
        self._enable_kcp = enable_kcp
        self._crl_hz = crl_hz
        self._device_id = device_id
        
        self._status_lock = threading.Lock()
        self._data_lock = threading.Lock()

        # data 
        self.info = {}
        self._cmd_queue = deque()
        
        # self.status = ControllerStatus.Disconnected
        self._send_barrier:Optional[threading.Barrier] = None
        self._complete_action_barrier:Optional[threading.Barrier] = None
        self.thread_is_alive = True
        
        if self._local_port == 0:
            raise ValueError("local_port must be greater than 0")
        
        # if self._device_id == 0:
        #     raise ValueError("device_id must be greater than 0")
        
    
    # @abstractmethod
    # def connect(self):
    #     pass
    
    @abstractmethod
    def start(self) -> bool:
        pass
    
    @abstractmethod
    def shutdown(self):
        pass
    
    @abstractmethod
    def all_brake(self):
        pass
    
    def put_command(self, cmd):
        self._cmd_queue.append(cmd)
        
    @abstractmethod
    def send_command(self):
        pass
    
    @abstractmethod
    def set_coordinator(self, barrier: threading.Barrier):
        pass
    
    @abstractmethod
    def get_info(self):
        pass
    
    @abstractmethod
    def get_thread_is_alive(self):
        pass
    
    @abstractmethod
    def get_status(self):
        pass
    
    @abstractmethod
    def _task_loop(self):
        pass

    