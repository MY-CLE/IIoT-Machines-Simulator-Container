from datetime import datetime
from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}

@app.route('/api/db')
def getLine():
    conn = sqlite3.connect("database/machine-sim.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO error (error_type) VALUES ('error1'), ('error');")
    return {'error': cursor.execute("SELECT error_type FROM error").fetchall()}