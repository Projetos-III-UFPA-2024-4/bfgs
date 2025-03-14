# Step 1: Add modules to provide access to specific libraries and functions
import json
import os # Module provides functions to handle file paths, directories, environment variables
import sys # Module provides access to Python-specific system parameters and functions
import myfunctions

# Step 2: Establish path to SUMO (SUMO_HOME)
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")
    

# Step 3: Add Traci module to provide access to specific libraries and functions
import traci # Static network information (such as reading and analyzing network files)

# Step 4: Define Sumo configuration
with open("config_sumo.json","r") as file:
    config = json.load(file)

Sumo_config = [
    config["sumo_binary"],
    '-c', config["config_file"],
    '--step-length', config["step_length"],
    '--delay', config["delay"],
    '--lateral-resolution', config["delay"]
]

# Step 5: Open connection between SUMO and Traci
traci.start(Sumo_config)

# Step 6: Define Variables

my_edge = 'Via3ToInter' #Aqui é onde mudados para qual via queremos analisar

# Step 7: Define Functions



traffic_lights = myfunctions.getAllTrafficLights()

# **Exibir a estrutura detectada**
print("\n📌 Semáforos e Vias Detectadas:")
for tls_id, data in traffic_lights.items():
    print(f"\n🔹 Semáforo: {tls_id}")
    print(f"   - Tempo de ciclo: {data['time_window']} segundos")
    for edge, lanes in data["edges"].items():
        print(f"   - Via: {edge} | Faixas: {lanes}")

# Step 8: Take simulation steps until there are no more vehicles in the network
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep() # Move simulation forward 1 step
    # Here you can decide what to do with simulation data at each s
    step = traci.simulation.getTime()

    for tls_id, data in traffic_lights.items():
        time_window = data["time_window"]
        edges = data["edges"]

        if step % time_window == 0:
            Y_values = myfunctions.getCriticalFlowRatio(edges,time_window)
            Y_total = sum(Y_values.values())

            C_o = myfunctions.calculate_webster_cycle(Y_total)

            print(f"\nStep {step}: Critical Flow Ratios (Y_i) para {tls_id}")
            for edge, Y_i in Y_values.items():
                print(f" - {edge}: {Y_i:.4f}")            

# Step 9: Close connection between SUMO and Traci
traci.close()