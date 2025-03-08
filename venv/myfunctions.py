import traci

def getNumberOfCarsInEdges(edge): #Pega o número de carros em uma via
    num_cars = 0
    if edge in traci.edge.getIDList():
        num_cars = traci.edge.getLastStepVehicleNumber(edge)

def getGreenPhases(tlsID):
    temp = traci.trafficlight.getCompleteRedYellowGreenDefinition(tlsID)
    temp = temp[0].phases
    num_phases = int(len(temp)/2)
    return num_phases

def getUsefuledges():
    edgesID = traci.edge.getIDList()
    usefuledgesID = [item for item in edgesID if not item.startswith(":cluster")]
    return usefuledgesID

def getCriticalFlowRatio(edges, time_window):
    critical_flow_ratios = {}

    for edgeID in edges:
        total_vehicles = 0
        for _ in range(time_window):
            total_vehicles += traci.edge.getLastStepVehicleNumber(edgeID)

        observed_vol = total_vehicles * (3600/time_window)

        max_flow = []
        for _ in range(time_window):
            flow_rate = traci.edge.getLastStepVehicleNumber(edgeID) * (3600/time_window)
            max_flow.append(flow_rate)

        saturation_flow = max(max_flow) if max_flow else 1

        critical_flow = observed_vol/saturation_flow
        critical_flow_ratios[edgeID] = critical_flow 

        return critical_flow_ratios   