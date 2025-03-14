import traci

def getNumberOfCarsInEdges(edge): #Pega o número de carros em uma via
    num_cars = 0
    if edge in traci.edge.getIDList():
        num_cars = traci.edge.getLastStepVehicleNumber(edge)

def getGreenPhases(tlsID):
    temp = traci.trafficlight.getAllProgramLogics(tlsID)
    temp = temp[0].phases
    num_phases = int(len(temp)/2)
    return num_phases

def getUsefuledges():
    edgesID = traci.edge.getIDList()
    usefuledgesID = [item for item in edgesID if not item.startswith(":cluster")]
    return usefuledgesID

def getAllTrafficLights():
    traffic_lighs = {}
    tls_ids = traci.trafficlight.getIDList()

    for tls_id in tls_ids:
        phases = traci.trafficlight.getAllProgramLogics(tls_id)[0].phases
        time_window = sum(phase.duration for phase in phases)

        controlled_links = traci.trafficlight.getControlledLinks(tls_id)

        edge_lanes = {}
        for link in controlled_links:
            if link:
                full_lane_id = link[0][0]
                edge_id = "_".join(full_lane_id.split("_")[:-1])

                if edge_id not in edge_lanes:
                    edge_lanes[edge_id] = []
                edge_lanes[edge_id].append(full_lane_id)

        traffic_lighs[tls_id] = {"edges": edge_lanes, "time_window": time_window}

    return traffic_lighs

def calculate_webster_cycle(Y):
    """Calcula o tempo ótimo de ciclo (C_o) usando a fórmula de Webster."""
    L = 20
    
    if Y >= 1:  # Evita erro de divisão por zero
        return 60  # Define um valor fixo de ciclo se Y >= 1
    
    C_o = (1.5 * L + 5) / (1 - Y)
    return round(C_o, 2)  # Retorna o valor arredondado

def calculate_green_time(Y_values, C_o, lost_time, phase_groups):
    """
    Calcula o tempo de verde para cada fase garantindo que vias na mesma direção tenham o mesmo tempo.
    """

    Y_total = sum(Y_values.values())  # Soma total de Y_i
    effective_green_time = C_o - lost_time  # Tempo disponível para verde

    if Y_total == 0:
        print(f"⚠️ Y_total = 0! Ajustando para evitar divisão por zero.")
        Y_total = 1  # Evita divisão por zero

    # Criar um dicionário para armazenar os tempos de verde por fase
    phase_green_times = {}

    for phase, edges in phase_groups.items():
        phase_Y_total = sum(Y_values.get(edge, 0) for edge in edges)  # Soma dos Y_i do grupo
        
        # Se a fase não tem fluxo crítico, garantir um mínimo de tempo verde
        if phase_Y_total == 0:
            phase_Y_total = 0.05  # Pequeno valor para evitar tempo 0
        
        phase_time = (phase_Y_total / Y_total) * effective_green_time  # Tempo total para a fase
        phase_time = max(phase_time, 5)  # 🔹 Garante um mínimo de 5s por fase

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
        if phase.state.count("G") > 0:  # Consideramos apenas fases que têm verde (G)
            active_edges = set()

            # Verifica quais vias estão liberadas na fase atual
            for i, link_group in enumerate(controlled_links):
                if phase.state[i] == "G":  # Se a posição do link for verde nessa fase
                    for link in link_group:
                        edge = link[0]  # Pegamos a via de origem
                        active_edges.add(edge)

            if active_edges:
                phase_groups[f"fase_{phase_index}"] = list(active_edges)

    return phase_groups

'''
def getCriticalFlowRatio(edges, time_window):
    critical_flow_ratios = {}
    time_window = int(time_window)

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
'''

def getCriticalFlowRatio(edge_lanes, time_window):
    """Calcula os valores de Y_i considerando o fluxo máximo do ciclo anterior."""
    historical_max_flow = {}  # Precisamos manter o histórico entre ciclos
    critical_flow_ratios = {}

    for edgeID, lanes in edge_lanes.items():
        total_vehicles = 0

        # Somar fluxo de todas as faixas da via no ciclo atual
        for laneID in lanes:
            total_vehicles += traci.lane.getLastStepVehicleNumber(laneID)

        # Fluxo observado normalizado pelo máximo do ciclo anterior
        max_past_flow = historical_max_flow.get(edgeID, total_vehicles)  # Se não há histórico, usa o próprio valor

        # Calcular v_i como a relação entre o fluxo atual e o maior fluxo registrado
        v_i = total_vehicles / max_past_flow if max_past_flow > 0 else 1.0

        # Atualizar o histórico com o maior fluxo já observado
        historical_max_flow[edgeID] = max(historical_max_flow.get(edgeID, 0), total_vehicles)

        # O fluxo de saturação agora é baseado no ciclo anterior
        s_i = historical_max_flow[edgeID]  # Usa o valor registrado no último ciclo

        # Calcular o Critical Flow Ratio (Y_i)
        Y_i = v_i / s_i if s_i > 0 else 0  # Evita divisão por zero
        critical_flow_ratios[edgeID] = Y_i  # Mantém precisão sem exagero

    return critical_flow_ratios

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
