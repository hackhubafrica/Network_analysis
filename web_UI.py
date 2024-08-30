from flask import Flask, render_template , request
import sqlite3
import requests

app = Flask(__name__)


# Implements Pagination
@app.route('/')
def index():
    page = int(request.args.get('page', 1))  # Get the current page number
    per_page = 20  # Number of packets per page
    offset = (page - 1) * per_page

    conn = sqlite3.connect('packets.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM packets')
    total_count = c.fetchone()[0]

    c.execute('SELECT * FROM packets ORDER BY timestamp DESC LIMIT ? OFFSET ?', (per_page, offset))
    packets = c.fetchall()
    conn.close()

    total_pages = (total_count + per_page - 1) // per_page  # Calculate total pages
    return render_template('web_UI.html', packets=packets, page=page, total_pages=total_pages)



@app.route('/packets')
def packets_api():
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page

    conn = sqlite3.connect('packets.db')
    c = conn.cursor()
    c.execute('SELECT * FROM packets ORDER BY timestamp DESC LIMIT ? OFFSET ?', (per_page, offset))
    packets = c.fetchall()
    conn.close()

    return {'packets': packets}


if __name__ == "__main__":
    app.run(debug=True)


# You can use libraries like Chart.js or D3.js to add charts and graphs to your dashboard.
# modify so that the heading do not dis
