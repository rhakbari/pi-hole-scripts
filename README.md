# DNS Monitor Script

This script monitors the average ping to a specified host (e.g., Cloudflare DNS) and dynamically changes the DNS settings based on the ping performance. If the average ping exceeds a high threshold for a specified number of consecutive checks, it switches to an alternative DNS (e.g., Google DNS). Conversely, if the ping falls below a low threshold for consecutive checks, it switches back to the original DNS.

## Prerequisites

- The script is written in Bash and requires a Unix-like operating system (e.g., Linux, MacOS).
- Administrative privileges may be required to change DNS settings.

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rhakbari/dns-monitor-script.git
   ```
  
2. **Make the script executable:**

   ```bash
   chmod +x dns_monitor.sh
   ```

3. **Run the script in the background:**
   ```bash
   ./dns_monitor.sh &
   ```

# For Running the Python Script on Every Boot in Debian

This guide demonstrates how to set up a systemd service to run a Python script automatically on every boot in Debian.

## Prerequisites

- Debian-based distribution (e.g., Debian, Ubuntu)
- Python script to run on boot

## Steps

1. **Create a systemd Service File**:
   
   - Create a `.service` file for your Python script. For example, let's assume your Python script is named `tplink_dns.py`, and it's located in `/path/to/script`.
   
   - Open a terminal and create a file named `myscript.service` in the `/etc/systemd/system/` directory:
   
     ```bash
     sudo nano /etc/systemd/system/myscript.service
     ```

   - Add the following content to the `myscript.service` file:

     ```ini
     [Unit]
     Description=My Python Script Service
     After=multi-user.target

     [Service]
     Type=simple
     ExecStart=/usr/bin/python3 /path/to/script/tplink_dns.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```

   - Replace `/path/to/script` with the actual path to your Python script.

2. **Enable the Service**:
   
   - After creating the service file, reload systemd and enable the service:
   
     ```bash
     sudo systemctl daemon-reload
     sudo systemctl enable myscript.service
     ```

3. **Start the Service**:
   
   - Start the service immediately without rebooting:
   
     ```bash
     sudo systemctl start myscript.service
     ```

4. **Verification**:
   
   - You can check the status of the service using:
   
     ```bash
     sudo systemctl status myscript.service
     ```

   - Ensure that your script has the necessary permissions to execute and read any files it needs.


