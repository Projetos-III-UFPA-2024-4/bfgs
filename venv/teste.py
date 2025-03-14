# Step 1: Add modules to provide access to specific libraries and functions
import json
import os
import sys
import myfunctions

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

# Step 6: Define Traffic Lights
traffic_lights = myfunctions.getAllTrafficLights()

# **Exibir a estrutura detectada**
print("\n📌 Semáforos e Vias Detectadas:")
for tls_id, data in traffic_lights.items():
    print(f"\n🔹 Semáforo: {tls_id}")
    print(f"   - Tempo de ciclo: {data['time_window']} segundos")
    for edge, lanes in data["edges"].items():
        print(f"   - Via: {edge} | Faixas: {lanes}")
'''
phase_groups = {
    "fase_1": ["Via2ToInter", "Via4ToInter"],  # Direção Norte-Sul
    "fase_2": ["Via1ToInter", "Via3ToInter"],  # Direção Leste-Oeste
}
'''
# **Função para calcular tempo de verde**
def calculate_green_time(Y_values, C_o, lost_time, phase_groups, min_green_time=7):
    """
    Calcula o tempo de verde garantindo que vias na mesma direção tenham o mesmo tempo.
    - Aplica um tempo mínimo de verde para evitar ciclos muito curtos.
    """

    Y_total = sum(Y_values.values())  # Soma total de Y_i
    effective_green_time = C_o - lost_time  # Tempo disponível para verde

    if Y_total == 0:
        Y_total = 1  # Evita divisão por zero

    # Criar um dicionário para armazenar os tempos de verde por fase
    phase_green_times = {}

    for phase, edges in phase_groups.items():
        phase_Y_total = sum(Y_values.get(edge, 0) for edge in edges)  # Soma dos Y_i do grupo

        # Se a fase não tem fluxo crítico, garantir um tempo mínimo
        if phase_Y_total == 0:
            phase_Y_total = 0.05  # Pequeno valor para evitar tempo 0
        
        phase_time = (phase_Y_total / Y_total) * effective_green_time  # Tempo total para a fase
        phase_time = max(phase_time, min_green_time)  # 🔹 Garante um mínimo de `min_green_time` segundos por fase

        phase_green_times[phase] = round(phase_time, 2)

    # Criar um dicionário para armazenar os tempos de verde para cada via
    green_times = {}

    for phase, edges in phase_groups.items():
        for edge in edges:
            green_times[edge] = phase_green_times[phase]  # Todas as vias da fase recebem o mesmo tempo

    return green_times


def get_phase_groups(tls_id):
    """
    Obtém automaticamente as vias que pertencem a cada fase do semáforo.
    Retorna um dicionário onde cada fase tem um conjunto de vias associadas.
    """
    phase_groups = {}  # Dicionário onde as chaves são fases e os valores são listas de vias

    # Obtém todas as fases do semáforo
    phases = traci.trafficlight.getAllProgramLogics(tls_id)[0].phases

    # Obtém as conexões controladas pelo semáforo
    controlled_links = traci.trafficlight.getControlledLinks(tls_id)

    for phase_index, phase in enumerate(phases):
        active_edges = set()

        # Verifica quais vias estão liberadas na fase atual
        for i, link_group in enumerate(controlled_links):
            if phase.state[i] == "G":  # Se a posição do link for verde nessa fase
                for link in link_group:
                    edge = link[0]  # Pegamos a via de origem
                    edge_id = "_".join(edge.split("_")[:-1])  # Remove possíveis sufixos _0

                    active_edges.add(edge_id)

        if active_edges:
            phase_groups[f"fase_{phase_index}"] = list(active_edges)

    return phase_groups

# Step 8: Simulation Loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    step = traci.simulation.getTime()

    for tls_id, data in traffic_lights.items():
        time_window = int(data["time_window"])
        edges = data["edges"]

        # 🚦 Detecta automaticamente as fases do semáforo
        phase_groups = get_phase_groups(tls_id)

        if step % time_window == 0:
            Y_values = myfunctions.getCriticalFlowRatio(edges, time_window)
            Y_total = sum(Y_values.values())

            # Calcular o tempo perdido total (L)
            lost_time = 10  # Exemplo: 10s

            # Calcular o Tempo Ótimo de Ciclo (C_o)
            C_o = myfunctions.calculate_webster_cycle(Y_total)

            # Calcular o tempo de verde garantindo igualdade para vias na mesma direção
            green_times = calculate_green_time(Y_values, C_o, lost_time, phase_groups)

            print(f"\nStep {step}: 🚦 Cálculo de Webster para {tls_id}")
            print(f"   - Tempo Ótimo de Ciclo (C_o): {C_o} segundos")
            print(f"   - Tempo Perdido Total (L): {lost_time} segundos")
            for phase, edges in phase_groups.items():
                print(f"   - {phase}: {edges}")
                for edge in edges:
                    print(f"     - {edge}: Y_i = {Y_values.get(edge, 0):.4f}, Tempo de Verde = {green_times[edge]}s")

