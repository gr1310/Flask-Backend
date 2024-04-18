import sqlite3
from flask import Flask, render_template
app= Flask(__name__)

def get_db_connected():
    conn= sqlite3.connect('database.db')
    conn.row_factory= sqlite3.Row
    return conn

@app.route('/')
def display():
    conn= get_db_connected()
    query= conn.execute('SELECT * FROM RotateImage').fetchall()
    conn.close()
    print(query)
