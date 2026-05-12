import socket
import threading
import argparse
from queue import Queue

# Global lock to prevent threads from printing over each other
print_lock = threading.Lock()
# Queue to hold the ports we want to scan
port_queue = Queue()

def grab_banner(s):
    """Attempts to grab the service banner from an open port."""
    try:
        # Wait up to 2 seconds for the service to send a banner
        s.settimeout(2)
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        return banner
    except Exception:
        return ""

def scan_port(target_ip, port):
    """Scans a single port using connect_ex()."""
    try:
        # Create a raw TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # 1 second timeout for the connection attempt
        
        # connect_ex returns 0 if the connection is successful (port is open)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            banner = grab_banner(s)
            
            # Use the lock to ensure the print statement doesn't get scrambled by other threads
            with print_lock:
                if banner:
                    print(f"[+] Port {port} is OPEN | Banner: {banner}")
                else:
                    print(f"[+] Port {port} is OPEN")
        s.close()
    except socket.error:
        pass

def thread_worker(target_ip):
    """Worker function that continuously pulls ports from the queue to scan."""
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target_ip, port)
        port_queue.task_done()

def main():
    # Setup Command Line Arguments
    parser = argparse.ArgumentParser(description="Multithreaded Raw Socket Port Scanner")
    parser.add_argument("target", help="Target IP address (e.g., 192.168.1.1)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads to run")
    args = parser.parse_args()

    target_ip = args.target
    start_port = args.start
    end_port = args.end
    num_threads = args.threads

    print(f"[*] Starting scan on {target_ip}...")
    print(f"[*] Port range: {start_port}-{end_port} with {num_threads} threads.\n")

    # Load the queue with all the ports in the range
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Spawn the threads
    threads_list = []
    for _ in range(num_threads):
        thread = threading.Thread(target=thread_worker, args=(target_ip,))
        threads_list.append(thread)
        thread.start()

    # Wait for all threads to finish execution before exiting
    for thread in threads_list:
        thread.join()

    print("\n[*] Scan Complete.")

if __name__ == "__main__":
    main()