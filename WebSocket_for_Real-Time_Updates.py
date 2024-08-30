# Import necessary modules
from scapy.all import sniff, IP, TCP
import asyncio

# Global list to store packets
packets = []

# Packet callback function
def packet_callback(packet):
    global packets
    if IP in packet and TCP in packet:
        packets.append({
            'source_ip': packet[IP].src,
            'destination_ip': packet[IP].dst,
            'source_port': packet[TCP].sport,
            'destination_port': packet[TCP].dport,
        })

# Function to capture packets in a separate thread
def start_sniffing():
    sniff(prn=packet_callback, filter="tcp", store=0)

# Function to get the latest packets
def get_latest_packets():
    global packets
    return packets

# WebSocket handler
async def handle_websocket(websocket):
    while True:
        # Fetch the latest packets
        data = get_latest_packets()
        if data:
            await websocket.send(str(data))
        await asyncio.sleep(1)  # Send updates every second

# Start the WebSocket server
async def main():
    start_sniffing()  # Start packet sniffing
    async with websockets.serve(handle_websocket, 'localhost', 6789):
        await asyncio.Future()  # Run forever

# Run the event loop
if __name__ == '__main__':
    import websockets
    asyncio.run(main())
