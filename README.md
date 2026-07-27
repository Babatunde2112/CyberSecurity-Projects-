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

## 🌐 Web Directory Brute Forcer

This project extends my reconnaissance toolkit by performing **web directory enumeration** after discovering HTTP or HTTPS services using my Port Scanner.

The objective is to automate the discovery of hidden or publicly accessible directories and files that may not be immediately visible through standard navigation.

---

### Lab Environment

To ensure testing was performed safely and ethically, all development and validation took place inside a self-hosted virtual lab.

**Infrastructure**

- Oracle VirtualBox (Hypervisor)
- Kali Linux (Attacking Machine)
- Ubuntu Server (Target Machine)
- Docker
- OWASP Juice Shop (Intentionally Vulnerable Web Application)

The Ubuntu Server was configured from scratch before Docker was installed. The OWASP Juice Shop application was then deployed inside a Docker container and verified to be accessible from the Kali Linux virtual machine before testing began.

---

### Testing Results

The Web Directory Brute Forcer successfully enumerated **directories/endpoints** on the OWASP Juice Shop application.

The majority of discovered resources returned an **HTTP 200 (OK)** response, indicating that the requested resources were accessible.

Depending on the application being tested, directory enumeration may also encounter response codes such as:

| Status Code | Meaning |
|-------------|---------|
| 200 | Resource found |
| 301 | Permanent redirect |
| 302 | Temporary redirect |
| 307 | Temporary redirect |
| 308 | Permanent redirect |
| 401 | Authentication required |
| 403 | Access forbidden |
| 404 | Resource not found |
| 405 | Method not allowed |
| 429 | Rate limited |
| 500 | Internal server error |
| 502 | Bad gateway |
| 503 | Service unavailable |

---

### Skills Demonstrated

- Python scripting
- Web reconnaissance
- Directory enumeration
- HTTP protocol analysis
- Virtual lab deployment
- Docker container deployment
- Ubuntu Server administration
- Kali Linux
- Ethical penetration testing methodology

---

### Disclaimer

This project was developed and tested **exclusively within a self-hosted, isolated laboratory environment** using the intentionally vulnerable **OWASP Juice Shop** application. No unauthorized systems, networks, or third-party infrastructure were targeted during development or testing.

---

### 💻 Usage Instructions

**Syntax:**
```bash
python3 dir_bruteforcer.py [http://192.168.1.10:3000](http://192.168.1.10:3000) /usr/share/wordlists/dirb/common.txt