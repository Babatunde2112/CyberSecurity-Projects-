import requests
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class DirectoryBruteForcer:
    def __init__(self, target_url, wordlist_path, threads=10, status_codes=[200, 301, 302, 401, 403]):
        self.target_url = target_url
        self.wordlist_path = wordlist_path
        self.threads = threads
        self.status_codes = status_codes
        self.found = []
    
    def test_directory(self, directory):
        """Test a single directory"""
        test_url = f"{self.target_url.rstrip('/')}/{directory.strip()}/"
        
        try:
            response = requests.get(test_url, timeout=5, allow_redirects=False)
            
            if response.status_code in self.status_codes:
                print(f"[+] Found: {test_url} (Status: {response.status_code})")
                self.found.append((test_url, response.status_code))
                return True
        except requests.exceptions.RequestException:
            pass
        
        return False
    
    def start(self):
        """Start the brute force scan"""
        try:
            with open(self.wordlist_path, 'r') as f:
                wordlist = f.readlines()
        except FileNotFoundError:
            print(f"[-] Wordlist not found: {self.wordlist_path}")
            return
        
        print(f"[*] Starting scan on {self.target_url}")
        print(f"[*] Using wordlist: {self.wordlist_path}")
        print(f"[*] Threads: {self.threads}\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.test_directory, word) for word in wordlist]
            
            for future in as_completed(futures):
                future.result()
        
        print(f"\n[*] Scan Complete! Found {len(self.found)} directories")
        return self.found

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python brute_forcer.py <target_url> [wordlist_path] [threads]")
        sys.exit(1)
    
    target = sys.argv[1]
    wordlist = sys.argv[2] if len(sys.argv) > 2 else "wordlists/SecLists/Discovery/Web-Content/common.txt"
    threads = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    forcer = DirectoryBruteForcer(target, wordlist, threads=threads)
    forcer.start()