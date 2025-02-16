import traci

# Inicie o SUMO com TraCI
traci.start(["sumo", "-c", r'data\myintersection.sumocfg'])

# Pegando todos os IDs dos semáforos

def getIDtls():
    return print("IDs dos semáforos:", traci.trafficlight.getIDList())

def getIdedges():
    return print("IDs das Vias:", traci.edge.getIDList())

getIdedges()
# Finaliza a simulação
traci.close()
