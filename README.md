# 🛡️ CyberSecurity-Projects-

Welcome to my cybersecurity portfolio. This repository serves as a practical testing ground for my journey into ethical hacking, defensive security, and network analysis. Instead of relying solely on pre-built tools, I built this space to focus on practical, real-world case studies by engineering custom scripts and automation tools from scratch. 

The projects within this repository bridge the gap between academic theory and practical application, demonstrating a core understanding of low-level networking, secure coding practices, and vulnerability assessment.

---

## 🛠️ Project 1: Multithreaded Network Scanner & Banner Grabber (`scanner.py`)

A high-speed, custom-built reconnaissance tool written in Python. This script performs raw socket port scanning to identify open pathways on a target machine, utilizing multi-threading to ensure rapid execution. Beyond basic scanning, it performs active banner grabbing to identify specific software versions running on open ports, aiding in vulnerability discovery.

### 🌟 Key Features
*   **High-Speed Concurrency:** Utilizes Python's `threading` and `Queue` modules to execute concurrent port checks, bypassing the slow, linear approach of traditional script execution.
*   **Active Banner Grabbing:** Implements socket `recv(1024)` logic with custom timeouts to capture service headers (e.g., extracting `SSH-2.0-OpenSSH` instead of just identifying Port 22).
*   **Intelligent Service Mapping:** Incorporates a fallback dictionary for common ports. If a service intentionally suppresses its banner, the script automatically maps the port to its standard protocol (e.g., mapping Port 80 to HTTP).
*   **Graceful Error Handling:** Uses `connect_ex()` for silent error management during closed-port encounters, ensuring the script runs flawlessly without crashing on strict firewalls.
*   **Automated Reporting:** Features an `-o` flag to seamlessly export structured scan results to a text file for post-engagement analysis.

### 💻 Usage Instructions

The tool is driven by command-line arguments for dynamic targeting. 

**Syntax:**
```bash
python3 scanner.py <TARGET_IP> -s <START_PORT> -e <END_PORT> -t <THREADS> -o <OUTPUT_FILE>