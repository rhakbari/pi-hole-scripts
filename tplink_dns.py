import subprocess
import time
from datetime import datetime

def get_average_ping(hostname):
    count = 4
    result = subprocess.run(["ping", "-c", str(count), hostname], capture_output=True, text=True)

    if result.returncode == 0:
        avg_ping = result.stdout.splitlines()[-1].split('/')[4]
        return avg_ping
    else:
        return "Error during ping"

def change_router_dns(dns_server):
    # Replace the following URL, username, and password with your router's details
    router_url = "http://192.168.0.1"
    router_username = "your_username"
    router_password = "your_password"

    # Set the DNS settings
    dns_payload = {"DnsSaVe": "0", "dns1": dns_server, "dns2": ""}
    session.post(f"{router_url}/userRpm/WanDnsCfgRpm.htm", data=dns_payload, auth=(router_username, router_password))

def log_dns_change(new_dns):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("dns_change_log.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] DNS changed to {new_dns}\n")

cloudflare_dns = ["1.1.1.1", "1.0.0.1"]
google_dns = ["8.8.8.8", "8.8.4.4"]

current_dns_servers = cloudflare_dns

host_to_ping = "1.1.1.1"
high_ping_threshold = 60  # ms
low_ping_threshold = 20  # ms
consecutive_checks = 5  # consecutive checks before changing DNS
sleep_interval = 60  # seconds

consecutive_high_pings = 0
consecutive_low_pings = 0

while True:
    avg_ping = get_average_ping(host_to_ping)
    print(f"Average Ping: {avg_ping} ms")

    if float(avg_ping) > high_ping_threshold:
        consecutive_high_pings += 1
        consecutive_low_pings = 0
    elif float(avg_ping) < low_ping_threshold:
        consecutive_low_pings += 1
        consecutive_high_pings = 0
    else:
        consecutive_high_pings = 0
        consecutive_low_pings = 0

    if consecutive_high_pings >= consecutive_checks:
        print(f"High ping for {consecutive_checks} consecutive checks. Changing DNS to Google...")
        current_dns_servers = google_dns

        # Change router DNS settings here
        change_router_dns(current_dns_servers[0])

        # Log DNS change
        log_dns_change(current_dns_servers[0])

        # Reset consecutive counts
        consecutive_high_pings = 0
        consecutive_low_pings = 0
    elif consecutive_low_pings >= consecutive_checks:
        print(f"Low ping for {consecutive_checks} consecutive checks. Changing DNS to Cloudflare...")
        current_dns_servers = cloudflare_dns

        # Change router DNS settings here
        change_router_dns(current_dns_servers[0])

        # Log DNS change
        log_dns_change(current_dns_servers[0])

        # Reset consecutive counts
        consecutive_high_pings = 0
        consecutive_low_pings = 0

    time.sleep(sleep_interval)
