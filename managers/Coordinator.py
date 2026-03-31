from typing import Optional, List
import threading

from .BaseCoordinator import BaseCoordinator
from ..controllers.ArmController import ArmController as Controller

class Coordinator(BaseCoordinator):
    
    def __init__(self, device_ws_url_list: Optional[List[dict]] = None, enable_kcp: bool = False):
        super().__init__()
        
        self._coordinator_monitor_loop = None
        self._enable_kcp = enable_kcp
        
        
        self.start(device_ws_url_list, enable_kcp)
    
    def start(self, device_ws_url_list, enable_kcp):
        if device_ws_url_list is None:
            print("device ip list is None")
            return False
        
        # create controllers
        for idx, ip in enumerate(device_ws_url_list):
            controller = Controller(
                ws_url=ip,
                local_port=0,
                enable_kcp=enable_kcp,
                crl_hz=500,
                device_id=idx
            )
            self._controllers_list.append(controller)
        
        # event init
        print(f"controllers {len(self._controllers_list)}")
        self._send_barrier = threading.Barrier(len(self._controllers_list)+1)
        self._complete_action_barrier = threading.Barrier(len(self._controllers_list)+1)
        
        # set coordinator to controllers
        for controller in self._controllers_list:
            controller.set_coordinator(self._send_barrier, self._complete_action_barrier)
        
        # controllers start
        for controller in self._controllers_list:
            controller.start()
        
        # # # coordinator thread start
        # self._coordinator_monitor_loop: threading.Thread = threading.Thread(target=self._monitor_loop)
        # self._coordinator_monitor_loop.start()
    
    
    def shutdown(self):
        self._stop_event.set()
        
        # controllers stop
        with self.controller_lock:
            for controller in self._controllers_list:
                controller.shutdown()
            
        # coordinator thread stop
        self._coordinator_monitor_loop.join(timeout=2)
        self._coordinator_monitor_loop = None
        
        
    def _monitor_loop(self):
        
        while not self._stop_event.is_set():
            alive = [c.get_device_id() for c in self._controllers_list if c.is_alive()]
            dead  = list(self.get_dead_threads().keys())
 
            if dead:
                print(f"[Monitor] 存活: {alive}  已退出: {dead}")
 
            self._stop_event.wait(timeout=1.0)
    
    
    # ============ command ==============
    def publish_command(self,cmd):
        try:
            
            with self.controller_lock:
                for controller in self._controllers_list:
                    controller.put_command(cmd)
                    
            # wait for controllers to finish
            if self._send_barrier:
                self._send_barrier.wait()
                print("all controllers execute command")
                
            # wait for controllers to finish
            if self._complete_action_barrier:
                self._complete_action_barrier.wait()
                print("all controllers complete action")
                
        except Exception as e:
            print(e)
    
    def all_brake_command(self):
        pass

    def all_home_command(self):
        pass