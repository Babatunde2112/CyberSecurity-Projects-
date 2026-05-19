import socket
import threading
import argparse
from queue import Queue

print_lock = threading.Lock()
port_queue = Queue()

def grab_banner(s):
    try:
        s.settimeout(2)
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        return banner
    except Exception:
        return ""

# WE ADDED an output_file parameter here
def scan_port(target_ip, port, output_file):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            banner = grab_banner(s)
            
            # Format the output string
            if banner:
                result_string = f"[+] Port {port} is OPEN | Banner: {banner}"
            else:
                result_string = f"[+] Port {port} is OPEN"
                
            with print_lock:
                print(result_string) # Print to terminal
                
                # WE ADDED file writing logic here
                if output_file:
                    with open(output_file, "a") as f:
                        f.write(result_string + "\n")
        s.close()
    except socket.error:
        pass

# WE ADDED the output_file parameter to the worker
def thread_worker(target_ip, output_file):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target_ip, port, output_file)
        port_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="Multithreaded Raw Socket Port Scanner")
    parser.add_argument("target", help="Target IP address (e.g., 192.168.1.1)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads to run")
    
    # WE ADDED the new argument flag here
    parser.add_argument("-o", "--output", type=str, help="Save results to a specified text file")
    
    args = parser.parse_args()

    target_ip = args.target
    start_port = args.start
    end_port = args.end
    num_threads = args.threads
    output_file = args.output

    print(f"[*] Starting scan on {target_ip}...")
    print(f"[*] Port range: {start_port}-{end_port} with {num_threads} threads.\n")

    # If the user specified an output file, clear it/create it before starting
    if output_file:
        with open(output_file, "w") as f:
            f.write(f"Scan Results for {target_ip}\n")
            f.write("="*30 + "\n")

    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    threads_list = []
    for _ in range(num_threads):
        # We pass the output_file to the worker here
        thread = threading.Thread(target=thread_worker, args=(target_ip, output_file))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    print("\n[*] Scan Complete.")
    if output_file:
        print(f"[*] Results saved to {output_file}")

if __name__ == "__main__":
    main()