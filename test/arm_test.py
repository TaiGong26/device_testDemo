import argparse
import traceback
import threading
import signal
import time
import sys

from hex_device_testDemo.managers.Coordinator import Coordinator




# clean up
def cleanup(coordinator):
    coordinator.shutdown()
    coordinator._stop_event.wait()

# 信号处理回调
def signal_handler(signal, frame, stop_event: threading.Event):
    print(f"[Signal] {signal} received, exit")
    stop_event.set()
    
    return

def main():
    # 标准库中获取命令行参数：数组
    parser = argparse.ArgumentParser(
        description='Hexapod robotic arm trajectory planning and execution test',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # array of device ip list
    parser.add_argument(
        '--url', 
        metavar='URL',
        default="ws://0.0.0.0:8439",
        help='WebSocket URL for HEX device connection, example: ws://0.0.0.0:8439 or ws://[::1%%eth0]:8439'
    )
    
    parser.add_argument(
        '--KCP', 
        action='store_true',
        default=False,
        help='Enable KCP protocol for HEX device connection'
    )
    
    # =============== parse args ===============
    args = parser.parse_args()
    dev_ip_list = list(args.url.split(','))
    enable_kcp = args.KCP
        
    stop_event = threading.Event()
    coordinator = None
    try:
        coordinator = Coordinator(dev_ip_list, enable_kcp)
        
        # 信号处理
        signal.signal(signal.SIGINT, lambda signal, frame: signal_handler(signal, frame, stop_event))
        signal.signal(signal.SIGTERM, lambda signal, frame: signal_handler(signal, frame, stop_event))
        
        # publish a command
        time.sleep(1)
        coordinator.publish_command([0, 0, 0, 0, 0, 0])
        print(f"publish command: {0, 0, 0, 0, 0, 0}")
        
        stop_event.wait()   
        # if coordinator is not None:
        #     cleanup(coordinator)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        
    except Exception as e:
        print(f"main error: {e}")
        traceback.print_exc()
    finally:
        # 恢复默认信号处理
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        
        if coordinator is not None:
            cleanup(coordinator)
        print("[finally] you can try a gain ctrl c to exit the terminal")
        sys.exit(0)

def r():
    raise ValueError("devic 0: test error")

def test():
    # dic = {}
    
    # print(dic.get("url"))
    try:
        r()
    except ValueError as e:
        print(e)
    
        
if __name__ == "__main__":
    main()
    # test()