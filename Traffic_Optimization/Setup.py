import os # Module provides functions to handle file paths, directories, environment variables
import sys # Module provides access to Python-specific system parameters and functions
import algorithm as al

# Step 2: Establish path to SUMO (SUMO_HOME)
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# Step 3: Add Traci module to provide access to specific libraries and functions
import traci # Static network information (such as reading and analyzing network files)
'''
Sumo_config = [
    "sumo_gui",
    '-c', config["config_file"],
    '--step-length', config["step_length"],
    '--delay', config["delay"],
    '--lateral-resolution', config["delay"]
]'''

# Step 5: Open connection between SUMO and Traci
traci.start(["sumo-gui", "-c", "teste\dteste.sumocfg"])

# Step 6: Define Variables

#my_edge = 'Via3ToInter' #Aqui é onde mudados para qual via queremos analisar

# Step 7: Define Functions
'''
def getNumberOfCarsInEdges(edge): #Pega o número de carros em uma via
    num_cars = 0
    if edge in traci.edge.getIDList():
        num_cars = traci.edge.getLastStepVehicleNumber(edge)
        print(f"Número de carros na via {edge}: {num_cars}")
'''
id = traci.trafficlight.getIDList()
controlled_lanes = traci.trafficlight.getControlledLanes(id[0])
phs = 0
steps = 0
of_ac = [0,0]
of = [0,0]
n_phases = 2
# Step 8: Take simulation steps until there are no more vehicles in the network traci.simulation.getMinExpectedNumber()
for i in range(100):
    
    of_ac[0] += traci.edge.getLastStepVehicleNumber(traci.lane.getEdgeID(controlled_lanes[0]))
    of_ac[1] += traci.edge.getLastStepVehicleNumber(traci.lane.getEdgeID(controlled_lanes[2]))

    
    if phs != traci.trafficlight.getPhase(id[0]):
        of[0] = (of_ac[0]/steps)
        of[1] = (of_ac[1]/steps)
        print(of)
        of_ac = [0,0]
        steps = 0
    
    '''all_crtclflw = 0
    sf = [1800, 1800] #1800 default
    for i in range(len(of)):
        all_crtclflw += of[i]/sf[i]
    edges = ['a', 'b']
    lost_time = (2 * 2) + 13
    sinal = al.Trffclght(n_phases, all_crtclflw, of, sf, edges)'''

    phs = traci.trafficlight.getPhase(id[0])
    traci.simulationStep()
    steps += 1


# Step 9: Close connection between SUMO and Traci
traci.close()