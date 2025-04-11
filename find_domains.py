#!/usr/bin/env python3

import subprocess
import ipaddress
import re
import sys

# Function to get IP addresses using dig
def dig_ips(domain):
    ipv4 = subprocess.run(["dig", "+short", "A", domain], capture_output=True, text=True).stdout.splitlines()
    ipv6 = subprocess.run(["dig", "+short", "AAAA", domain], capture_output=True, text=True).stdout.splitlines()
    return ipv4 + ipv6

# Function to get CIDR ranges from whois
def get_cidr_from_whois(ip):
    try:
        result = subprocess.run(["whois", ip], capture_output=True, text=True).stdout
        match = re.search(r"(CIDR|inetnum|NetRange):\s+([^\n]+)", result, re.IGNORECASE)
        if match:
            raw = match.group(2).strip()
            if "/" in raw:
                return raw
            elif "-" in raw:
                start_ip, end_ip = raw.split("-")
                start_ip = ipaddress.ip_address(start_ip.strip())
                end_ip = ipaddress.ip_address(end_ip.strip())
                networks = ipaddress.summarize_address_range(start_ip, end_ip)
                return ", ".join(str(net) for net in networks)
        return None
    except Exception:
        return None

# Function to get unique CIDR ranges
def get_unique_cidrs(domain):
    ips = dig_ips(domain)
    cidrs = set()
    for ip in ips:
        result = get_cidr_from_whois(ip)
        if result:
            for cidr in result.split(","):
                cidrs.add(cidr.strip())
    return sorted(cidrs)

# Function to handle adding or removing websites from the whitelist
def modify_whitelist(whitelist):
    print("\nWould you like to:")
    print("1) Remove websites from whitelist")
    print("2) Add websites to whitelist")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        websites_to_remove = input("\nEnter websites to remove, separated by commas: ").strip()
        if websites_to_remove:
            websites_list = [website.strip() for website in websites_to_remove.split(",")]
            for website in websites_list:
                if website in whitelist:
                    whitelist.remove(website)
                    print(f"Removed {website} from whitelist.")
                else:
                    print(f"{website} was not found in the whitelist.")
        else:
            print("No websites entered for removal.")

    elif choice == "2":
        websites_to_add = input("\nEnter websites to add, separated by commas: ").strip()
        if websites_to_add:
            websites_list = [website.strip() for website in websites_to_add.split(",")]
            for website in websites_list:
                if website not in whitelist:
                    whitelist.append(website)
                    print(f"Added {website} to whitelist.")
                else:
                    print(f"{website} is already in the whitelist.")
        else:
            print("No websites entered for addition.")

    else:
        print("Invalid choice. Please enter 1 or 2.")

    return whitelist

def main():
    # Default whitelist (you can persist it if you want)
    whitelist = []

    # Ask the user whether they'd like to modify the whitelist
    modify_choice = input("Would you like to modify the whitelist? (y/n): ").strip().lower()

    if modify_choice == "y":
        whitelist = modify_whitelist(whitelist)

    # Display the updated whitelist
    if whitelist:
        print("\nUpdated Whitelist:")
        for website in whitelist:
            print(f"  - {website}")
    else:
        print("No websites in the whitelist.")

    # Ask for the domain after modifying the whitelist
    domain = input("\nEnter a domain to get IP ranges (e.g., wikipedia.org): ").strip()

    # Process the domain if provided
    if domain:
        print(f"\nFinding IP ranges for: {domain}")
        cidrs = get_unique_cidrs(domain)
        if cidrs:
            print("CIDR ranges found:")
            for cidr in cidrs:
                print(f"  - {cidr}")
        else:
            print("No CIDR ranges found.")

if __name__ == "__main__":
    main()
