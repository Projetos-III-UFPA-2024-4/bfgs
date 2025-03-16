from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql

app = Flask(__name__)
CORS(app)  # Permite requisições do Flutter

# Conectar ao banco de dados MySQL remoto
db = mysql.connector.connect(
    host="your_remote_host",  # IP ou domínio do servidor MySQL
    user="your_user",
    password="your_password",
    database="your_database"
)

cursor = db.cursor(dictionary=True)

# Endpoint para buscar usuários
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

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
