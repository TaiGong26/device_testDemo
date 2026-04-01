from hex_device import HexDeviceApi
import threading
from hex_device import Arm, CommandType

from .BaseController import BaseController
import time
from dataclasses import dataclass
from enum import Enum


"""
状态机
 - Disconnected
 - Init
 - Ready
 - Running
 - HoldPosition
 - Stopped
 - Error
 - Exit

"""

class ArmControllerStatus(Enum):
    Disconnected    = 0
    Init            = 1       # init device
    Ready           = 2       # waiting command
    Running         = 3       # running command
    Brake           = 4       # brake
    Error           = 5       # error
    Exit            = 6       # output logger

class ArmExecutorStatus(Enum):
    Disconnected    = 0
    Ready           = 1
    Running         = 2
    HoldPosition    = 3
    Stopped         = 4
    Error           = 5


class ArmController(BaseController):
    def __init__(self, ws_url:str, local_port:int=0, enable_kcp:bool=False, crl_hz:int=500, device_id:int=0):
        super().__init__(ws_url, local_port, enable_kcp, crl_hz, device_id)
        
        self._hex_api = None
        self._task_thread = None
        self.device = None
        self.status = ArmControllerStatus.Disconnected
       
    # def connect(self):
    #     pass
    
    def start(self) -> bool:
        
        self._hex_api = HexDeviceApi(
            ws_url=self._ws_url, 
            local_port=0, 
            enable_kcp=self._enable_kcp, 
            )
        
        self._task_thread = threading.Thread(target=self._task_loop,daemon=True)
        self._task_thread.start()
        
        # add wait for device list to be updated
        while not self._hex_api.device_list:
            time.sleep(0.1)
            
        for device in self._hex_api.device_list:
            print(f"[Device {self._device_id}] 发现设备: {device} type: {type(device)}")
            if isinstance(device, Arm):
                self.device = device
                with self._status_lock:
                    self.status = ArmControllerStatus.Init
                if device.robot_type:
                    self.robot_type = device.robot_type
                    # print(f"[Device {self._device_id}] 设备类型: {self.robot_type}")
                break
        if self.device is None:
            print("device is None")
            return False
        self.device.start()
        
        with self._status_lock:
            self.status = ArmControllerStatus.Ready
        
        return True
   
    def shutdown(self):
        try:
            if self._task_thread:
                if self._task_thread.is_alive():
                    self._task_thread.join(timeout=0.1)
            self._task_thread = None
            if self._hex_api:
                self._hex_api.close()
            self._hex_api = None
            
            print(f"[Device {self._device_id}]------------------------------------ shutdown")
        except RuntimeError as e:
            print(f"[Device {self._device_id}, RuntimeError]: {e}")
        
        except Exception as e:
            print(f"[Device {self._device_id}, Exception]: {e}")
        
    def set_barrier(self, _send_barrier, _complete_action_barrier):
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
        
            while True: # what is the condition: hex_device_api is running
                
                try:
                    
                    # status machine
                    
                    
                    
                    # update controller info
                    
                    
                    
                    # update device info
                    
                    
                    # check this controller is connected
                    # waiting for coordinator sync
                    # if self._send_barrier:
                    #     self._send_barrier.wait()
                    
                    # this controller send command or send message
                    self.send_command()
                    # if self._complete_action_barrier:
                    #     self._complete_action_barrier.wait()
                    
                    # update info
                    
                    
                    # ============= test ===========
                    print(f"[Device {self._device_id}] motor position: {self.device.get_motor_positions()}")
                    
                    time.sleep(0.01)
                    
                    # print(f"[Device {self._device_id}] motor position: {self.device.get_motor_positions()}")
                    
                    # raise Exception("test")
                
                except Exception as e:
                    print(f"[Device {self._device_id}] 线程异常崩溃: {e}")
                
                    
                
        
        except Exception as e:
            print(f"[Device {self._device_id}] 线程异常崩溃: {e}")
            # event delegation
        finally:
            print(f"[Device {self._device_id}] 任务线程退出")
        
    def send_command(self) -> bool:
        
        if self._send_barrier is None or self._complete_action_barrier is None:
            raise ValueError("coordinator is None")
            
        if self._send_barrier:
            self._send_barrier.wait()
            
        cmd = self._cmd_queue.get()
            
        # send command
        self.device.motor_command( # device inner have a lock
            CommandType.POSITION,
            cmd
        )
        
        # wait for complete action
        if self._complete_action_barrier:
            self._complete_action_barrier.wait()
        
        if cmd is None:
            return False
        return True

def main():
    pass

if __name__ == "__main__":
    main()