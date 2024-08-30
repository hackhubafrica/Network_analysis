from scapy.all import sniff, IP, TCP

# Dictionary to store count of SYN requests from each IP
syn_count = {}

def packet_callback(packet):
    if packet.haslayer(TCP):
        if packet[TCP].flags == 'S':  # SYN flag
            src_ip = packet[IP].src
            if src_ip in syn_count:
                syn_count[src_ip] += 1
            else:
                syn_count[src_ip] = 1
            
            # Example condition: Flag if more than 100 SYN packets from the same IP
            if syn_count[src_ip] > 100:
                print(f"Potential SYN Flood detected from {src_ip}!")

# Start sniffing and apply the callback
sniff(filter="tcp", prn=packet_callback, count=1000)
