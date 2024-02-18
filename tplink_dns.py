import subprocess
import time
from datetime import datetime

def get_average_ping(hostname):
    count = 4
    result = subprocess.run(["ping", "-c", str(count), hostname], capture_output=True, text=True)

    if result.returncode == 0:
        avg_ping = result.stdout.splitlines()[-1].split('/')[4]
        return float(avg_ping)
    else:
        return None
        
def change_router_dns(dns_server):
    # Replace the following URL and password with your router's details
    router_url = "http://192.168.0.1"
    router_password = "your_password"

    # Set the DNS settings
    dns_payload = {"DnsSaVe": "0", "dns1": dns_server, "dns2": ""}
    response = requests.post(f"{router_url}/userRpm/WanDnsCfgRpm.htm", data=dns_payload, auth=("admin", router_password))

    if response.status_code == 200:
        print("Router login successful.")
    else:
        print("Router login failed.")

def get_router_dns():
    # Replace the following URL, username, and password with your router's details
    router_url = "http://192.168.0.1"
    router_username = "your_username"
    router_password = "your_password"

    # Get the current DNS settings
    # You may need to use a different method to fetch router DNS settings based on your router's API
    # This is just a placeholder
    # Modify this part according to your router's API or web interface
    # Example: Use requests library to fetch DNS settings from router's web interface
    # dns_settings = requests.get(f"{router_url}/dns_settings", auth=(router_username, router_password)).json()
    # return dns_settings["dns_servers"]

    # For now, return None as a placeholder
    return None

def log_dns_change(new_dns):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("dns_change_log.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] DNS changed to {new_dns}\n")

cloudflare_dns = ["1.1.1.1", "1.0.0.1"]
google_dns = ["8.8.8.8", "8.8.4.4"]

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

    if avg_ping is not None:
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
            print(f"High ping for {consecutive_checks} consecutive checks.")

            # Get the current DNS settings from the router
            current_dns_servers = get_router_dns()

            # If DNS is not set or set to an invalid value, set it to Google DNS
            if not current_dns_servers or current_dns_servers not in [cloudflare_dns, google_dns]:
                print("Router DNS not set or set to an invalid value. Setting to Google DNS.")
                current_dns_servers = google_dns
                change_router_dns(current_dns_servers[0])
                log_dns_change(current_dns_servers[0])
            else:
                print("Router DNS is already set.")

            # Reset consecutive counts
            consecutive_high_pings = 0
            consecutive_low_pings = 0
        elif consecutive_low_pings >= consecutive_checks:
            print(f"Low ping for {consecutive_checks} consecutive checks.")

            # Get the current DNS settings from the router
            current_dns_servers = get_router_dns()

            # If DNS is not set or set to an invalid value, set it to Cloudflare DNS
            if not current_dns_servers or current_dns_servers not in [cloudflare_dns, google_dns]:
                print("Router DNS not set or set to an invalid value. Setting to Cloudflare DNS.")
                current_dns_servers = cloudflare_dns
                change_router_dns(current_dns_servers[0])
                log_dns_change(current_dns_servers[0]))
            else:
                print("Router DNS is already set.")

            # Reset consecutive counts
            consecutive_high_pings = 0
            consecutive_low_pings = 0
    else:
        print("Error during ping. Skipping DNS check.")

    time.sleep(sleep_interval)
