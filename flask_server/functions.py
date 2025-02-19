import traci

def getNumberOfCarsInEdges(edge): #Pega o número de carros em uma via
    num_cars = 0
    if edge in traci.edge.getIDList():
        num_cars = traci.edge.getLastStepVehicleNumber(edge)
        print(f"Número de carros na via {edge}: {num_cars}")