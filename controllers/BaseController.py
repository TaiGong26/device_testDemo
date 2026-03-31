from abc import ABC, abstractmethod
import asyncio
from typing import Optional, List
import threading
# from collections import deque
from queue import Queue
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
        
        self.robot_type =None
        
        self._status_lock = threading.Lock()
        self._data_lock = threading.Lock()

        # data 
        self.controll_info = {}
        self.device_info = {}
        self._cmd_queue = Queue()
        
        # self.status = ControllerStatus.Disconnected
        self._send_barrier:Optional[threading.Barrier] = None
        self._complete_action_barrier:Optional[threading.Barrier] = None
        self.thread_is_alive = True
        
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
    
    def put_command(self, cmd:Optional[list[float]] = None) -> bool:
        if self._cmd_queue.full():
            return False
        self._cmd_queue.put(cmd)
        return True
        
    @abstractmethod
    def send_command(self) -> bool:
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
    
    def get_device_id(self):
        with self._status_lock:
            return self._device_id
        
    def get_controll_info(self):
        with self._status_lock:
            return self.controll_info
    
    def get_device_info(self):
        with self._status_lock:
            return self.device_info
    
    @abstractmethod
    def _task_loop(self):
        pass

    