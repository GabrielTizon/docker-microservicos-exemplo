from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root'),
        database=os.environ.get('DB_NAME', 'testdb')
    )

def init_db():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            idade INT,
            cidade VARCHAR(100)
        );
    """)
    db.commit()
    cursor.close()
    db.close()

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    nome = data.get('nome')
    idade = data.get('idade')
    cidade = data.get('cidade')
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (nome, idade, cidade) VALUES (%s, %s, %s)", (nome, idade, cidade))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'status': 'sucesso'})

@app.route('/users', methods=['GET'])
def list_users():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(users)

if __name__ == '__main__':
    # Espera o banco estar pronto e inicializa a tabela
    for _ in range(10):
        try:
            init_db()
            print("Banco inicializado!")
            break
        except Exception as e:
            print(f"Banco ainda não está pronto, tentando novamente... {e}")
            time.sleep(5)
    app.run(host='0.0.0.0', port=5001)
