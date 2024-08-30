import sqlite3

def create_tables():
    conn = sqlite3.connect('packets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_ip TEXT,
            destination_ip TEXT,
            source_port INTEGER,
            destination_port INTEGER,
            length INTEGER,
            payload TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
