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
    """
    Cria um novo Post-it.
    ---
    parameters:
      - name: titulo
        in: formData
        type: string
        required: true
      - name: data
        in: formData
        type: string
        format: date
        required: true
      - name: descricao
        in: formData
        type: string
        required: false
    responses:
      201:
        description: Post-it criado
        examples:
          application/json: { "id": 1, "titulo": "Reunião", "data": "14-10-2025", "descricao": "Reunião com a equipe as 8h" }
    """
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

@app.route('/lembretes', methods=['GET'])
def listar_lembretes():
    """
    Lista todos os Post-it.
    ---
    responses:
      200:
        description: Lista de Post-it
        examples:
          application/json: [ { "id": 1, "titulo": "Reunião", "data": "14-10-2025", "descricao": "Reunião com a equipe as 8h" } ]
    """
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM lembretes').fetchall()
    conn.close()
    return jsonify([
        {"id": r["id"], "titulo": r["titulo"], "data": r["data"], "descricao": r["descricao"]}
        for r in rows
    ])

@app.route('/lembretes/<int:id>', methods=['PUT'])
def editar_anotacao(id):
    """
    Edita um Post-it existente.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: titulo
        in: formData
        type: string
        required: false
      - name: data
        in: formData
        type: string
        format: date
        required: false
      - name: descricao
        in: formData
        type: string
        required: false
    responses:
      200:
        description: Post-it editado
        examples:
          application/json: { "id": 1, "titulo": "Reunião", "data": "14-10-2025", "descricao": "Reunião com a equipe as 8h" }
      404:
        description: Post-it não encontrado.
    """
    conn = get_db_connection()
    anotacao = conn.execute('SELECT * FROM lembretes WHERE id = ?', (id,)).fetchone()
    if anotacao is None:
        conn.close()
        return jsonify({"error": "Anotação não encontrada"}), 404
    titulo = request.form.get('titulo', anotacao['titulo'])
    data = request.form.get('data', anotacao['data'])
    descricao = request.form.get('descricao', anotacao['descricao'])
    conn.execute(
        'UPDATE lembretes SET titulo = ?, data = ?, descricao = ? WHERE id = ?',
        (titulo, data, descricao, id)
    )
    conn.commit()
    conn.close()
    return jsonify({"id": id, "titulo": titulo, "data": data, "descricao": descricao})

@app.route('/lembretes/<int:id>', methods=['DELETE'])
def excluir_anotacao(id):
    """
    Exclui um Post-it.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Post-it excluído
        examples:
          application/json: { "result": "Post-it excluído" }
      404:
        description: Post-it não encontrado
    """
    conn = get_db_connection()
    cur = conn.execute('DELETE FROM lembretes WHERE id = ?', (id,))
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": "Anotação não encontrada"}), 404
    conn.close()
    return jsonify({"result": "Anotação excluída"})

@app.route('/lembretes/<int:id>', methods=['GET'])
def consultar_anotacao(id):
    """
    Consulta um Post-it específico.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Dados do Post-it
        examples:
          application/json: { "id": 1, "titulo": "Reunião", "data": "14-10-2025", "descricao": "Reunião com a equipe as 8h" }
      404:
        description: Post-it não encontrado
    """
    conn = get_db_connection()
    anotacao = conn.execute('SELECT * FROM lembretes WHERE id = ?', (id,)).fetchone()
    conn.close()
    if anotacao is None:
        return jsonify({"error": "Anotação não encontrada"}), 404
    return jsonify({
        "id": anotacao["id"],
        "titulo": anotacao["titulo"],
        "data": anotacao["data"],
        "descricao": anotacao["descricao"]
    })

if __name__ == '__main__':
    app.run(debug=True)