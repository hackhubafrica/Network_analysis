from scapy.all import sniff, TCP, IP

def packet_callback(packet):
    # Check if the packet has a TCP layer and port 80 (HTTP)
    if packet.haslayer(TCP) and packet[TCP].dport == 80:
        print(f"HTTP Packet: {packet[IP].src} -> {packet[IP].dst}")

# Start sniffing on the default interface, filtering for HTTP packets
sniff(filter="tcp port 80", prn=packet_callback, count=10)
