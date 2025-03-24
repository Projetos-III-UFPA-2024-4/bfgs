import traci
import json
import mysql.connector
from TrafficCollector import TrafficCollector
from Controller import controller_flow

def main():
    # === Carrega configurações ===
    with open("config_sumo.json", "r") as sumo_file:
        sumo_config = json.load(sumo_file)

    with open("config_db.json", "r") as db_file:
        db_config = json.load(db_file)

    # === Inicia conexão com banco de dados ===
    cnx = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )
    cur = cnx.cursor(buffered=True)


    # === Inicia o SUMO ===
    sumo_args = [
        sumo_config["sumo_binary"],
        "-c", sumo_config["config_file"],
        "--step-length", sumo_config["step_length"],
        "--delay", sumo_config["delay"],
        "--lateral-resolution", sumo_config["lateral_resolution"]
    ]

    traci.start(sumo_args)

    collector = TrafficCollector("Tl1")

    step = 0
    # === Loop principal da simulação ===
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step = traci.simulation.getTime()  # Obtém o tempo atual da simulação
        # Executa a coleta de dados
        collector.collect(cur, cnx, db_config, step)

        # Executa o controle
        #controller_flow(cur, db_config)
    
    # === Encerra a simulação e o banco ===
    traci.close()
    cur.close()
    cnx.close()

if __name__ == "__main__":
    main()