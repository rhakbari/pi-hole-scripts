#!/bin/bash

# Function to get the average ping 
get_average_ping() {
    local hostname=$1
    local count=4
    local result
    result=$(ping -c "$count" "$hostname" 2>&1)

    # Check if the ping was successful
    if [[ $? -eq 0 ]]; then
        # Extract the average ping time from the output
        local avg_ping=$(echo "$result" | grep -oP 'avg=\K[^/]+')
        echo "$avg_ping"
    else
        echo "Error during ping"
    fi
}

# Function to change Pi-hole DNS settings
change_pihole_dns() {
    local dns_server=$1
    pihole status
    pihole -a -d "$dns_server"
    pihole restartdns
}

cloudflare_dns=("1.1.1.1" "1.0.0.1")
google_dns=("8.8.8.8" "8.8.4.4")

current_dns_servers=("${cloudflare_dns[@]}")

host_to_ping="1.1.1.1"
high_ping_threshold=60  # ms
low_ping_threshold=20  # ms
consecutive_checks=5  # consecutive checks before changing DNS
sleep_interval=60  # seconds

consecutive_high_pings=0
consecutive_low_pings=0

while true; do
    avg_ping=$(get_average_ping "$host_to_ping")
    echo "Average Ping: $avg_ping ms"

    if (( $(echo "$avg_ping > $high_ping_threshold" | bc -l) )); then
        ((consecutive_high_pings++))
        consecutive_low_pings=0
    elif (( $(echo "$avg_ping < $low_ping_threshold" | bc -l) )); then
        ((consecutive_low_pings++))
        consecutive_high_pings=0
    else
        consecutive_high_pings=0
        consecutive_low_pings=0
    fi

    if ((consecutive_high_pings >= consecutive_checks)); then
        echo "High ping for $consecutive_checks consecutive checks. Changing DNS to Google..."
        current_dns_servers=("${google_dns[@]}")

        # Change Pi-hole DNS settings here
        change_pihole_dns "${current_dns_servers[0]}"

        # Reset consecutive counts
        consecutive_high_pings=0
        consecutive_low_pings=0
    elif ((consecutive_low_pings >= consecutive_checks)); then
        echo "Low ping for $consecutive_checks consecutive checks. Changing DNS to Cloudflare..."
        current_dns_servers=("${cloudflare_dns[@]}")

        # Change Pi-hole DNS settings here
        change_pihole_dns "${current_dns_servers[0]}"

        # Reset consecutive counts
        consecutive_high_pings=0
        consecutive_low_pings=0
    fi

    sleep "$sleep_interval"
done
