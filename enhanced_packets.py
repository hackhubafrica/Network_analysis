from scapy.all import sniff, IP, TCP
import datetime

# Callback function called by scapy for every captured packet
def packet_callback(packet):
    # Check if the packet has an IP layer and TCP layer
    if packet.haslayer(IP) and packet.haslayer(TCP):
        ip_layer = packet[IP]
        tcp_layer = packet[TCP]
        
        # Get packet details
        source_ip = ip_layer.src
        destination_ip = ip_layer.dst
        source_port = tcp_layer.sport
        destination_port = tcp_layer.dport
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Print packet details
        print(f"[{timestamp}] Captured packet:")
        print(f"  Source IP: {source_ip}")
        print(f"  Destination IP: {destination_ip}")
        print(f"  Source Port: {source_port}")
        print(f"  Destination Port: {destination_port}")
        print(f"  Packet Length: {len(packet)} bytes")
        print(f"  Payload (truncated): {bytes(packet[TCP].payload)[:50]}...")
        print('-' * 50)

# Start capturing packets with a filter for HTTP traffic (port 80)
def start_sniffing():
    try:
        print("Starting packet capture...")
        sniff(filter="tcp port 80", prn=packet_callback, count=1, store=0)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_sniffing()




