from flask import Flask, jsonify, request
from flasgger import Swagger
import sqlite3
from flask_cors import CORS
import os


app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'agenda.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS lembretes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            data DATE NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()