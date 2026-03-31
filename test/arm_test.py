import argparse
import traceback
import threading
import signal


from hex_device_testDemo.managers.Coordinator import Coordinator




# clean up
def cleanup(coordinator):
    coordinator.shutdown()
    print("[Cleanup] shutdown")

# 信号处理回调
def signal_handler(signal, frame, stop_event: threading.Event, coordinator):
    cleanup(coordinator)
    print(f"[Signal] {signal} received, exit")
    stop_event.set()

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
    
    try:
        coordinator = Coordinator(dev_ip_list, enable_kcp)
        
        # 信号处理
        signal.signal(signal.SIGINT, lambda signal, frame: signal_handler(signal, frame, stop_event, coordinator))
        signal.signal(signal.SIGTERM, lambda signal, frame: signal_handler(signal, frame, stop_event, coordinator))
        
        stop_event.wait()
    except KeyboardInterrupt:
        print("keyboard interrupt")
        
    except Exception as e:
        print(f"main error: {e}")
        traceback.print_exc()
    
def test():
    dic = {}
    
    print(dic.get("url"))
        
    
        
if __name__ == "__main__":
    main()
    # test()