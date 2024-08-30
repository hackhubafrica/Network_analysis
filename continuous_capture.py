from scapy.all import sniff, IP, TCP
import sqlite3
import datetime

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('packets.db')
    return conn

# Callback function to handle and store packets
def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        ip_layer = packet[IP]
        tcp_layer = packet[TCP]
        
        # Extract packet details
        source_ip = ip_layer.src
        destination_ip = ip_layer.dst
        source_port = tcp_layer.sport
        destination_port = tcp_layer.dport
        payload = bytes(packet[TCP].payload).decode(errors='ignore')[:50]
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        length = len(packet)

        # Store packet data in the database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO packets (timestamp, source_ip, destination_ip, source_port, destination_port, length, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, source_ip, destination_ip, source_port, destination_port, length, payload))
        conn.commit()
        conn.close()

        # Print packet details
        print(f"[{timestamp}] Captured packet:")
        print(f"  Source IP: {source_ip}")
        print(f"  Destination IP: {destination_ip}")
        print(f"  Source Port: {source_port}")
        print(f"  Destination Port: {destination_port}")
        print(f"  Packet Length: {length} bytes")
        print(f"  Payload (truncated): {payload}...")
        print('-' * 50)

def start_sniffing():
    try:
        print("Starting continuous packet capture...")
        sniff(prn=packet_callback, store=0)  # Runs indefinitely
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_sniffing()
