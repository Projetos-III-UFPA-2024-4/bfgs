import os # Module provides functions to handle file paths, directories, environment variables
import sys # Module provides access to Python-specific system parameters and functions
from Semaforo import Semaforo

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
traci.start(["sumo-gui", "-c", "simulation_config/2025-02-18-01-43-58/osm.sumocfg"])

# Step 6: Define Variables

#my_edge = 'Via3ToInter' #Aqui é onde mudados para qual via queremos analisar

# Step 7: Define Functions

def getNumberOfCarsInEdges(edge): #Pega o número de carros em uma via
    num_cars = 0
    if edge in traci.edge.getIDList():
        num_cars = traci.edge.getLastStepVehicleNumber(edge)
        print(f"Número de carros na via {edge}: {num_cars}")

# Step 8: Take simulation steps until there are no more vehicles in the network traci.simulation.getMinExpectedNumber()
for i in range(50):
    traci.simulationStep() # Move simulation forward 1 step
    id = traci.trafficlight.getIDList()

    print(traci.trafficlight.getPhaseDuration(id[0]))
    ''' + traci.trafficlight.getNextSwitch(id[0]) - traci.simulation.getTime()'''
    print(traci.trafficlight.getAllProgramLogics(id[0]))


    # Here you can decide what to do with simulation data at each step
    #getNumberOfCarsInEdges(my_edge)
    # step_count = step_count + 1

# Step 9: Close connection between SUMO and Traci
traci.close()