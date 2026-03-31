from abc import ABC, abstractmethod
import asyncio
from typing import Optional, List
import threading
from collections import deque

# 控制器状态机
class CoordinatorStatus:
    NoneStatus = 0
    Init = 1
    Ready = 2
    Running = 3
    Stopped = 4
    Error = 5
    Exit = 6

class BaseCoordinator(ABC):
    def __init__(self):
        # self._async_loop = None
        # self._device_ws_url_list = _device_ws_url_list
        
        self._stop_event = threading.Event()
        self.controller_lock = threading.Lock()
        self._send_barrier:Optional[threading.Barrier] = None
        self._complete_action_barrier:Optional[threading.Barrier] = None
        
        self._controllers_list = deque()
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def publish_command(self):
        pass
    
    @abstractmethod
    def all_brake_command(self):
        pass
    
    @abstractmethod
    def all_home_command(self):
        pass