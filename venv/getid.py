#Criei esse code para podemos pegar os ids de algo que a gente precise
import traci

# Inicie o SUMO com TraCI
traci.start(["sumo", "-c", r'data\myintersection.sumocfg'])


# Pegando todos os IDs dos semáforos
def getIDtls():
    return print("IDs dos semáforos:", traci.trafficlight.getIDList())

# Pegando todos os IDs das vias
def getIdedges():
    return print("IDs das Vias:", traci.edge.getIDList())


# Finaliza a simulação
traci.close()
