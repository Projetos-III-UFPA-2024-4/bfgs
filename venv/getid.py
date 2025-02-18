#Criei esse code para podemos pegar os ids de algo que a gente precise
import traci
import json

# Inicie o SUMO com TraCI
with open("config_sumo.json","r") as file:
    config = json.load(file)

Sumo_config = [
    config["sumo_binary"],
    '-c', config["config_file"],
    '--step-length', config["step_length"],
    '--delay', config["delay"],
    '--lateral-resolution', config["delay"]
]

# Pegando todos os IDs dos semáforos
def getIDtls():
    return print("IDs dos semáforos:", traci.trafficlight.getIDList())

# Pegando todos os IDs das vias
def getIdedges():
    edges = traci.edge.getIDList()
    for edge in edges:
        print("IDs das Vias:", edges[edge])

def getNextTLS():
    return print()

if __name__ == "__main__":
    traci.start(Sumo_config)

    getIdedges()

    traci.close() # Finaliza a simulação
