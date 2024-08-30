from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

# Capture packets on the default network interface
sniff(prn=packet_callback, count=100)



