from flask import Flask, jsonify
import congestion_collector as collector
import threading

app = Flask(__name__)

collector_thread = None

@app.route('/start_collector', methods=['GET'])
def start_collector():
    global collector_thread

    if collector_thread and collector_thread.is_alive():
        return jsonify({"massage": "Coletor já está rodando"}), 400
    
    collector_thread = threading.Thread(target=collector.run, daemon=True)
    collector_thread.start()

    return jsonify({"message": "Coletor iniciado com sucesso!"})

@app.route('/')
def status():
    return jsonify({"message": "API do Coletor está rodando!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)