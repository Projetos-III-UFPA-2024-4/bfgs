from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permite requisições do Flutter

DBADDR = os.environ.get("DBADDR")
DBPORT = os.environ.get("DBPORT")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBTABLE = os.environ.get("DBTABLE")
DB = os.environ.get("DB")


# Conectar ao banco de dados MySQL remoto
db = mysql.connector.connect(
    host=DBADDR,  # IP ou domínio do servidor MySQL
    user=DBUSER,
    password=DBPASS,
    database=DB,
)

cursor = db.cursor(dictionary=True)

# Endpoint para buscar usuários
@app.route('/traffic-state', methods=['GET'])
def get_traffic_state():
    cursor.execute("SELECT * FROM congestion_state.traffic_updates")
    traffic_state = cursor.fetchall()
    return jsonify(traffic_state)

# Endpoint para adicionar um usuário
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({'error': 'Missing name or age'}), 400

    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    db.commit()
    return jsonify({'message': 'User added successfully'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
