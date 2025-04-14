#!/usr/bin/env python3

import subprocess
import ipaddress
import re
import json
import os

WHITELIST_FILE = "whitelist.json"

def dig_ips(domain):
    ipv4 = subprocess.run(["dig", "+short", "A", domain], capture_output=True, text=True).stdout.splitlines()
    ipv6 = subprocess.run(["dig", "+short", "AAAA", domain], capture_output=True, text=True).stdout.splitlines()
    return ipv4 + ipv6

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

def get_unique_cidrs(domain):
    ips = dig_ips(domain)
    cidrs = set()
    for ip in ips:
        result = get_cidr_from_whois(ip)
        if result:
            for cidr in result.split(","):
                cidrs.add(cidr.strip())
    return sorted(cidrs)

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, "r") as f:
            return json.load(f)
    return {}

def save_whitelist(whitelist):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(whitelist, f, indent=2)

def modify_whitelist(domains):
    print("\nWould you like to:")
    print("1) Remove websites from whitelist")
    print("2) Add websites to whitelist")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        to_remove = input("Enter websites to remove, separated by commas: ").strip()
        for site in [w.strip() for w in to_remove.split(",")]:
            domains.pop(site, None)
            print(f"Removed {site}")
    elif choice == "2":
        to_add = input("Enter websites to add, separated by commas: ").strip()
        for site in [w.strip() for w in to_add.split(",")]:
            if site not in domains:
                domains[site] = []
                print(f"Added {site}")
            else:
                print(f"{site} is already in the whitelist.")
    else:
        print("Invalid choice.")

    return domains

def update_domains_with_cidrs(domains):
    for domain in domains:
        print(f"\nGetting CIDRs for: {domain}")
        cidrs = get_unique_cidrs(domain)
        if cidrs:
            domains[domain] = cidrs
            print(f"  Found {len(cidrs)} CIDRs.")
        else:
            print("  No CIDRs found.")
    return domains

def main_domains():
    whitelist = load_whitelist()

    modify = input("Modify the whitelist? (y/n): ").strip().lower()
    if modify == "y":
        whitelist = modify_whitelist(whitelist)

    whitelist = update_domains_with_cidrs(whitelist)
    save_whitelist(whitelist)

    print("\nWhitelist saved to whitelist.json")

if __name__ == "__main__":
    main_domains()
