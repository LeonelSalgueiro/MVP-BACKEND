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

@app.route('/lembretes', methods=['POST'])
def criar_anotacao():
    titulo = request.form.get('titulo')
    data = request.form.get('data')
    descricao = request.form.get('descricao')
    if not titulo or not data:
        return jsonify({"error": "Título e data são obrigatórios"}), 400
    conn = get_db_connection()
    cur = conn.execute(
        'INSERT INTO lembretes (titulo, data, descricao) VALUES (?, ?, ?)',
        (titulo, data, descricao)
    )
    conn.commit()
    anotacao_id = cur.lastrowid
    conn.close()
    return jsonify({"id": anotacao_id, "titulo": titulo, "data": data, "descricao": descricao}), 201