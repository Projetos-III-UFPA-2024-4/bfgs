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

            print(f"\nStep {step}: 🚦 Atualizando tempos de semáforo para {tls_id}")
            print(f"   - Tempo Ótimo de Ciclo (C_o): {C_o} segundos")
            print(f"   - Tempo Perdido Total (L): {lost_time} segundos")

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

                # 📌 Printar a duração da nova fase antes de aplicar
                print(f"   - {phase}: Estado = {original_phase.state}, Tempo Ajustado = {phase_duration}s")

                # Modificar apenas a duração da fase original
                original_phase.duration = phase_duration
                modified_phases.append(original_phase)

            # 🔹 Aplicar a nova configuração do semáforo no SUMO
            new_logic = traci.trafficlight.Logic(current_logic.programID, 0, 0, modified_phases)
            traci.trafficlight.setCompleteRedYellowGreenDefinition(tls_id, new_logic)

    # 🔹 Coletar dados estatísticos
    for veh_id in traci.vehicle.getIDList():
        wait_time = traci.vehicle.getWaitingTime(veh_id)
        vehicle_wait_times[veh_id] = vehicle_wait_times.get(veh_id, 0) + wait_time
        total_wait_time += wait_time
        total_vehicles += 1

        if veh_id not in vehicle_travel_times:
            vehicle_travel_times[veh_id] = step  # Marca o tempo de entrada do veículo

    for edge_id in traci.edge.getIDList():
        queue_length = traci.edge.getLastStepHaltingNumber(edge_id)
        edge_queues[edge_id] = queue_length
        total_queue_length += queue_length
        num_edges += 1

    # Calcular tempo total de viagem dos veículos que saíram do sistema
    for veh_id in list(vehicle_travel_times.keys()):
        if veh_id not in traci.vehicle.getIDList():
            vehicle_travel_times[veh_id] = step - vehicle_travel_times[veh_id]

    # Armazena os dados coletados a cada step
    time_steps.append(step)
    avg_wait_times.append(total_wait_time / total_vehicles if total_vehicles else 0)
    avg_travel_times.append(sum(vehicle_travel_times.values()) / len(vehicle_travel_times) if vehicle_travel_times else 0)
    avg_queue_lengths.append(total_queue_length / num_edges if num_edges else 0)

# Fechar conexão com SUMO
traci.close()

# 📈 Gerar gráficos para análise

plt.figure(figsize=(12, 5))

# Tempo de espera nos semáforos
plt.subplot(1, 3, 1)
plt.plot(time_steps, avg_wait_times, label="Tempo médio de espera", color='red')
plt.xlabel("Tempo (s)")
plt.ylabel("Tempo médio de espera (s)")
plt.title("Tempo Médio de Espera nos Semáforos")
plt.legend()

# Tempo de viagem
plt.subplot(1, 3, 2)
plt.plot(time_steps, avg_travel_times, label="Tempo médio de viagem", color='blue')
plt.xlabel("Tempo (s)")
plt.ylabel("Tempo médio de viagem (s)")
plt.title("Tempo Médio de Viagem dos Veículos")
plt.legend()

# Tamanho médio da fila
plt.subplot(1, 3, 3)
plt.plot(time_steps, avg_queue_lengths, label="Tamanho médio da fila", color='green')
plt.xlabel("Tempo (s)")
plt.ylabel("Número médio de veículos esperando")
plt.title("Número Médio de Veículos Esperando")
plt.legend()

plt.tight_layout()
plt.show()
