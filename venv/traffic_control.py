import traci
from traci import trafficlight as tl
import json
import os
import traffic_utils

with open("config_sumo.json", "r") as sumo_file:
    config = json.load(sumo_file)

Sumo_config = [
    config["sumo_binary"],  # Caminho para o binário do SUMO
    '-c', config["config_file"],  # Arquivo de configuração do SUMO
    '--step-length', config["step_length"],  # Define o tempo de cada passo da simulação
    '--delay', config["delay"],  # Define o atraso na execução
    '--lateral-resolution', config["delay"],  # Define a resolução lateral
    '--start'
]

traci.start(Sumo_config)

traffic_light_id = "Tl1"

duracoes_verde = [40, 25, 30, 24]

traffic_utils.update_green_phases_manually(traffic_light_id, duracoes_verde)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
traci.close()