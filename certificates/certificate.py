import ssl
import socket
import OpenSSL
import os
import shutil
import json
from projects.project_context import get_current_project_number


current_project_number = get_current_project_number()
c_path = os.path.dirname(os.path.abspath(__file__))
certs_path = f"projects/{current_project_number}/certs"
domains_path = f"projects/{current_project_number}/allowed_domains.json"

os.makedirs(certs_path, exist_ok=True)

def get_domains_from_file(domains_file):
    """Load domains from the JSON file."""
    if not os.path.exists(domains_file):
        print(f"Error: Domains file '{domains_file}' not found.")
        return []
    with open(domains_file, "r") as f:
        try:
            data = json.load(f)
            return data.get("domains", [])
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from '{domains_file}'.")
            return []

def get_certificate(domain, port=443):
    conn = socket.create_connection((domain, port))
    context = ssl.create_default_context()
    with context.wrap_socket(conn, server_hostname=domain) as s:
        cert = s.getpeercert(True)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
        return x509

def save_certificate(domain):
    cert = get_certificate(domain)
    cert_file_path = f"{certs_path}/{domain}.crt"
    with open(cert_file_path, "wb") as f:
        f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
    print(f"Saved certificate for {domain} at {cert_file_path}")




def run_all_certificate():
    print("Running certificate commands. This may take a while...")
    domains = get_domains_from_file(domains_path)
    if not domains:
        print("No domains to process.")
        return
    for domain in domains:
        save_certificate(domain)

def __main__():
    run_all_certificate()