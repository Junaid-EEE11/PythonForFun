from flask import Flask, request, redirect, url_for, render_template
import sqlite3
from datetime import datetime
import pytz

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loaddata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                load TEXT NOT NULL,
                message TEXT NOT NULL,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

with app.app_context():
    init_db()

@app.route('/')
def index():
    entries = []
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, load, message, time FROM loaddata ORDER BY id DESC LIMIT 10')
        entries = cursor.fetchall()
    return render_template('form.html', entries=entries)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    load = request.form.get('load')
    message = request.form.get('message')
    time = request.form.get('time')

    # Convert local datetime to UTC
    if time:
        local_tz = pytz.timezone('America/New_York')
        local_time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        local_time = local_tz.localize(local_time)
        utc_time = local_time.astimezone(pytz.utc)
        time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    if name and load and message:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO loaddata (name, load, message, time) VALUES (?, ?, ?, ?)', (name, load, message, time))
            conn.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
