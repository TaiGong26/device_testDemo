from hex_device import HexDeviceApi
import threading
from hex_device import Arm, CommandType

from .BaseController import BaseController
"""
臂控制器
 - 统一连接
 - 统一启动
 - 统一命令发送
 
"""

class ArmController(BaseController):
    def __init__(self, ws_url:str, local_port:int=0, enable_kcp:bool=False, crl_hz:int=500, device_id:int=0):
        super().__init__(ws_url, local_port, enable_kcp, crl_hz, device_id)
        self._coordinator = None # Coordinator
        
        self._hex_api = None
        self._task_thread = None
        self.device = None
       
    # def connect(self):
    #     pass
    
    def start(self) -> bool:
        # if self._coordinator is None:
        #     # raise ValueError("coordinator is None")
        #     print("coordinator is None")
        #     return False
        
        self._hex_api = HexDeviceApi(self._ws_url, self._local_port, self._enable_kcp, self._crl_hz)
        
        self._task_thread = threading.Thread(target=self._task_loop)
        self._task_thread.start()
        
        for device in self._hex_api.device_list:
            if isinstance(device, Arm):
                self.device = device
                break
        if self.device is None:
            print("device is None")
            return False
        self.device.start()
        return True
   
    def shutdown(self):
        self._task_thread.join(timeout=2)
        self._task_thread = None
        self._hex_api.close()
        self._hex_api = None
    
    def set_coordinator(self, _send_barrier, _complete_action_barrier):
        self._send_barrier = _send_barrier
        self._complete_action_barrier = _complete_action_barrier
    
    def get_info(self):
        pass
    
    def get_status(self):
        pass
    
    def get_thread_is_alive(self):
        pass
    def _task_loop(self):
        try:
        
            while True: # what is the condition?
                
                # check this controller is connected
                
                
                # waiting for coordinator sync
                if self._coordinator_task_barrier:
                    self._coordinator_task_barrier.wait()
                
                # this controller send command or send message
                
                
                # update info
                
                pass
        
        except Exception as e:
            print(f"[Device {self._device_id}] 线程异常崩溃: {e}")
            # event delegation
        finally:
            print(f"[Device {self._device_id}] 任务线程退出")
        
    def send_command(self):
        
        if self._send_barrier is None or self._complete_action_barrier is None:
            raise ValueError("coordinator is None")
            
        cmd = None
        if self._cmd_queue:
            cmd = self._cmd_queue.popleft()
        
        if cmd is None:
            return
        # loop condition
        
        self._send_barrier.wait()
        # send command
        self.device.motor_command( # device inner have a lock
            CommandType.POSITION,
            cmd
        )
        
        # wait for complete action
        self._complete_action_barrier.wait()

    def all_brake(self):
        pass
    

def main():
    pass

if __name__ == "__main__":
    main()