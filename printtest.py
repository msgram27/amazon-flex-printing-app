import socket

def test_zebra(ip):
    zpl_test = """
^XA
^FO50,50^A0N,50,50^FDZebra ZD621^FS
^FO50,120^A0N,30,30^FDConnected!^FS
^FO50,180^B3N,N,100,Y,N^FDTEST_SUCCESS^FS
^XZ
"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((ip, 9100))
            sock.sendall(zpl_test.encode())
            print(f"✅ Success! Printing test label on {ip}")
            return True
    except Exception as e:
        print(f"❌ Failed to connect to {ip}: {e}")
        return False

# Replace with your IP
test_zebra("192.168.2.70")