import socket

def scan_port(ip, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)  # Set a timeout for the connection attempt
    
    try:
        # Attempt to connect to the IP address and port
        s.connect((ip, port))
        
        # If connection succeeds, close the socket and return True
        s.close()
        return True
    except:
        # If connection fails, close the socket and return False
        s.close()
        return False

def scan_network(ip_range, ports):
    # List to store discovered devices
    devices = []
    
    # Perform the scan for each IP address in the range
    for i in range(1, 255):
        ip = ip_range + "." + str(i)
        
        # Scan each port in the list
        for port in ports:
            if scan_port(ip, port):
                devices.append((ip, port))
                break  # Stop scanning other ports for this IP if one port is open
    
    return devices

# Specify your local network IP range
ip_range = "192.168.1"

# Specify a list of common ports to check
ports_to_check = [80, 443, 1883, 8883, 5683]

# Scan the network for devices with any of the specified ports open
devices_with_ports_open = scan_network(ip_range, ports_to_check)

# Print the list of devices found with open ports
if devices_with_ports_open:
    print("Devices found with open ports:")
    for device in devices_with_ports_open:
        print(f"IP: {device[0]}, Port: {device[1]}")
else:
    print("No devices found with open ports.")
