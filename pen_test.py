import socket

def basic_port_scan(target):
    ports = [21, 22, 23, 25, 53, 80, 443]
    print(f"Scanning {target}...")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open on {target}")
        sock.close()

if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    basic_port_scan(target)
