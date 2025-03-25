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

@app.route('/traffic-light-states', methods=['GET'])
def get_traffic_light_state():
    cursor.execute("SELECT * FROM congestion_state.traffic_light_states")
    traffic_light_states = cursor.fetchall()
    return jsonify(traffic_light_states)

#endpoint para modificar simulação
@app.route('/change-mode', methods=['POST'])
def change_mode():
    data = request.json
    mode = data.get('mode')

    if not mode:
        return jsonify({'error': 'Missing mode'}), 400
    cursor.execute("DELETE FROM traffic_updates_manual")
    cursor.execute("INSERT INTO traffic_updates_manual (id, phase_id, cycle_time, green_time, Num_Phases, mode) VALUES (1, 0, 0, 0, 0, %s)", (mode, ))
    db.commit()
    return jsonify({'message': 'Succesfully changed mode'})

@app.route('/traffic-change', methods=['POST'])
def send_data():
    data = request.json
    ide = data.get('ide')
    phase_id = data.get('phase_id')
    cycle_time = data.get('cycle_time')
    green_time = data.get('green_time')
   
    ide_a = data.get('ide_a')
    phase_id_a = data.get('phase_id_a')
    cycle_time_a = data.get('cycle_time_a')
    green_time_a = data.get('green_time_a')

    mode = data.get('mode')
    num_phase = data.get('Num_Phase')
    
    if not phase_id or not cycle_time or not green_time or not num_phase or not mode:
        return jsonify({'error': 'Missing parameters'}), 400
    cursor.execute("DELETE FROM traffic_updates_manual")

    
    cursor.execute("INSERT INTO traffic_updates_manual (id, phase_id, cycle_time, green_time, Num_Phases, mode) VALUES (%s,%s, %s, %s, %s, %s)", (ide, phase_id, cycle_time, green_time, num_phase, mode, ))
    cursor.execute("INSERT INTO traffic_updates_manual (id, phase_id, cycle_time, green_time, Num_Phases, mode) VALUES (%s,%s, %s, %s, %s, %s)", (ide_a, phase_id_a, cycle_time_a, green_time_a, num_phase, mode, ))
    db.commit()
    return jsonify({'message': 'Traffic change committed succesfully'})

@app.route('/notifications', methods=['GET'])
def get_notifications():
    cursor.execute("SELECT * FROM congestion_state.notifications")
    notifications = cursor.fetchall()
    return jsonify(notifications)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
