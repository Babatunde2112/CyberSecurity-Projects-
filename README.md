# 🛡️ CyberSecurity-Projects-

Welcome to my cybersecurity portfolio. This repository serves as a practical testing ground for my journey into ethical hacking, defensive security, and network analysis. Instead of relying solely on pre-built tools, I built this space to focus on practical, real-world case studies by engineering custom scripts and automation tools from scratch. 

The projects within this repository bridge the gap between academic theory and practical application, demonstrating a core understanding of low-level networking, secure coding practices, and vulnerability assessment.

---

## 🔬 Lab Environment & Ethical Testing

To ensure testing was performed safely and ethically, all development and validation took place inside a self-hosted virtual lab. No unauthorized systems, networks, or third-party infrastructure were targeted during development or testing.

**Infrastructure Used:**
*   **Hypervisor:** Oracle VirtualBox
*   **Attacking Machine:** Kali Linux
*   **Target Machine:** Ubuntu Server LTS
*   **Containerization:** Docker
*   **Target Application:** OWASP Juice Shop (Intentionally Vulnerable Web App)

The Ubuntu Server was configured from scratch, and the OWASP Juice Shop application was deployed inside a Docker container. Connectivity and routing were verified across a custom NAT Network prior to tool execution.

---

## 🗂️ Portfolio Projects

### 🛠️ Project 1: Multithreaded Network Scanner & Banner Grabber (`scanner.py`)
A high-speed, custom-built reconnaissance tool written in Python. This script performs raw socket port scanning to identify open pathways on a target machine. Beyond basic scanning, it performs active banner grabbing to identify specific software versions running on open ports, aiding in initial vulnerability discovery.

**Internal Features & Technical Capabilities:**
*   **High-Speed Concurrency:** Utilizes Python's `threading` and `Queue` modules to execute concurrent port checks, bypassing the slow, linear approach of traditional script execution.
*   **Active Banner Grabbing:** Implements socket `recv(1024)` logic with custom timeouts to capture service headers (e.g., extracting `SSH-2.0-OpenSSH` instead of just identifying Port 22).
*   **Intelligent Service Mapping:** Incorporates a fallback dictionary for common ports. If a service intentionally suppresses its banner, the script automatically maps the port to its standard protocol (e.g., mapping Port 80 to HTTP).
*   **Graceful Error Handling:** Uses `connect_ex()` for silent error management during closed-port encounters, ensuring the script runs flawlessly without crashing on strict firewalls.
*   **Automated Reporting:** Features an `-o` flag to seamlessly export structured scan results to a text file for post-engagement analysis.

**Usage Syntax:**
```bash
python3 scanner.py <TARGET_IP> -s <START_PORT> -e <END_PORT> -t <THREADS> -o <OUTPUT_FILE>

```

### 🌐 Project 2: Web Directory Brute Forcer (`dir_bruteforcer.py`)

A multithreaded web reconnaissance tool written in Python that performs automated directory enumeration against HTTP/HTTPS services. Designed to complement my Network Scanner, this utility discovers hidden directories, administrative panels, exposed files, and other accessible resources that are not immediately visible through standard web navigation.

**Internal Features & Technical Capabilities:**
* **HTTP Response Code Analysis:** Automatically evaluates server responses to categorize discovered resources, distinguishing between accessible pages (200 OK), redirects (301/302), forbidden content (403), and filtering out invalid paths (404).
* **Multithreaded Enumeration:** Utilizes Python's `threading` and `Queue` modules to concurrently process large wordlists, significantly improving enumeration speed.
* **Rate-Limit Throttling:** Supports configurable delays between requests to emulate realistic traffic patterns and reduce the likelihood of triggering server-side rate limiting (429 Too Many Requests).
* **Custom Wordlist Support:** Accepts user-defined wordlists through command-line arguments, allowing compatibility with common security wordlists such as DIRB and SecLists.
* **Robust Error Handling:** Gracefully manages connection failures, timeouts, and interrupted requests to ensure reliable execution during scans.

**Testing Results:**
The tool was successfully validated inside a self-hosted penetration testing lab built using Oracle VirtualBox. The lab consisted of a Kali Linux attack machine and an Ubuntu Server target running Docker with the intentionally vulnerable **OWASP Juice Shop** application. During testing, the scanner successfully enumerated approximately **1,976 candidate paths**, identifying numerous accessible resources (HTTP 200), redirects (301/302), and intentionally restricted directories (403), demonstrating accurate response classification.

**Usage Syntax:**

```bash
python3 dir_bruteforcer.py http://192.168.1.10:3000 /usr/share/wordlists/dirb/common.txt
```

**🧠 Skills Demonstrated**
* **Programming & Scripting:** Python CLI application development, multithreading, queue management, and exception handling.
* **Networking Protocols:** HTTP/HTTPS request handling, status code interpretation, and web application reconnaissance.
* **System Administration:** Oracle VirtualBox virtualization, Ubuntu Server deployment, Docker containerization, and Kali Linux operations.
* **Security Methodology:** Web directory enumeration, attack surface mapping, reconnaissance automation, and ethical penetration testing practices.