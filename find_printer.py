import socket
import threading
import time

def test_printer(ip_address):
    """Test if a device is a Zebra printer"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            result = sock.connect_ex((ip_address, 9100))
            if result == 0:
                print(f"✅ FOUND PRINTER at {ip_address}")
                return True
            else:
                print(f"❌ No printer at {ip_address}")
                return False
    except Exception as e:
        print(f"❌ Error testing {ip_address}: {e}")
        return False

# Test common Zebra IPs in your network range
common_ips = [
    '192.168.2.70', '192.168.2.77', '192.168.2.100', '192.168.2.101',
    '192.168.2.110', '192.168.2.116', '192.168.2.120', '192.168.2.130',
    '192.168.2.155', '192.168.2.159', '192.168.2.172', '192.168.2.196'
]

print("Scanning for Zebra printer on port 9100...")
for ip in common_ips:
    if test_printer(ip):
        break
else:
    print("No printer found on common IPs. Try the configuration print method.")