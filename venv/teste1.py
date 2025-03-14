import traci
import matplotlib.pyplot as plt
import myfunctions
import sys, os, json

# Dicionários para armazenar estatísticas ao longo do tempo
time_steps = []
avg_wait_times = []
avg_travel_times = []
avg_queue_lengths = []

vehicle_wait_times = {}  # Tempo total de espera por veículo
vehicle_travel_times = {}  # Tempo total de viagem por veículo
edge_queues = {}  # Tamanho da fila por via

# Step 2: Establish path to SUMO (SUMO_HOME)
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# Step 3: Add Traci module to provide access to SUMO functions
import traci 

# Step 4: Load SUMO configuration
with open("config_sumo.json", "r") as file:
    config = json.load(file)

Sumo_config = [
    config["sumo_binary"],
    '-c', config["config_file"],
    '--step-length', config["step_length"],
    '--delay', config["delay"],
    '--lateral-resolution', config["delay"]
]

# Step 5: Open connection between SUMO and TraCI
traci.start(Sumo_config)

traffic_lights = myfunctions.getAllTrafficLights()

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    step = traci.simulation.getTime()

    total_wait_time = 0
    total_vehicles = 0
    total_queue_length = 0
    num_edges = 0

    for tls_id, data in traffic_lights.items():
        time_window = int(data["time_window"])
        edges = data["edges"]

        # 🚦 Identificar automaticamente as fases do semáforo
        phase_groups = myfunctions.get_phase_groups(tls_id)

        if step % time_window == 0:
            Y_values = myfunctions.getCriticalFlowRatio(edges, time_window)
            Y_total = sum(Y_values.values())

            # Calcular o tempo perdido total (L)
            lost_time = 10  # Exemplo: 10s

            # Calcular o Tempo Ótimo de Ciclo (C_o)
            C_o = myfunctions.calculate_webster_cycle(Y_total)

            # Calcular o tempo de verde garantindo igualdade para vias na mesma direção
            green_times = myfunctions.calculate_green_time(Y_values, C_o, lost_time, phase_groups)

            # 🔴 Obter as fases existentes para modificar apenas os tempos
            current_logic = traci.trafficlight.getAllProgramLogics(tls_id)[0]
            modified_phases = []

            for phase_index, (phase, edges) in enumerate(phase_groups.items()):
                phase_duration = green_times[edges[0]]  # Tempo de verde baseado na primeira via do grupo

                # 🔹 Obter a fase original
                original_phase = current_logic.phases[phase_index]

                # 🔹 Identificar se é uma fase de amarelo ou verde
                if "y" in original_phase.state:
                    phase_duration = original_phase.duration  # Mantém o amarelo sem alterações
                else:
                    phase_duration += 3  # Adiciona o tempo de amarelo às fases de verde

                # Modificar apenas a duração da fase original
                original_phase.duration = phase_duration
                modified_phases.append(original_phase)

                print(original_phase,"\n")
                print(modified_phases.append(original_phase))


# Fechar conexão com SUMO
traci.close()