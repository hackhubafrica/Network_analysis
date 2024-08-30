import sqlite3
import time


# you might detect SYN flood attacks by counting the number of SYN packets from a single IP.

def check_anomalies():
    conn = sqlite3.connect('paxckets.db')
    c = conn.cursor()
    while True:
        # Example: Check for SYN flood attack
        c.execute('''
            SELECT source_ip, COUNT(*) as count
            FROM packets
            WHERE payload LIKE '%SYN%'
            GROUP BY source_ip
            HAVING count > 100
        ''')
        suspicious_ips = c.fetchall()
        if suspicious_ips:
            for ip, count in suspicious_ips:
                print(f"Alert! Suspicious activity from IP {ip}: {count} packets detected.")
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    check_anomalies()
