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
