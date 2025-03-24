import traci

def update_detector_counts(detectors, total_count):
    """
    Soma o número total de veículos detectados em todos os detectores durante a fase verde.

    Args:
        detectors (list[str]): Lista de IDs dos detectores de indução no cenário SUMO.
        total_count (int): Contador atual que acumula a quantidade de veículos.

    Returns:
        int: Valor atualizado de total_count com as detecções do passo atual somadas.
    """
    count = 0
    for detector in detectors:
        count = traci.inductionloop.getLastStepVehicleNumber(detector)
        total_count += count

    return total_count


def calculate_critical_flow(observed_flow, S_i=1800):
    """
    Calcula o fluxo crítico com base no número de veículos observados e na capacidade de saturação.

    Args:
        observed_flow (int or float): Número total de veículos detectados na fase verde.
        S_i (int, optional): Capacidade de saturação da via (veículos/hora). Padrão: 1800.

    Returns:
        float: Valor do fluxo crítico (observed_flow / S_i).
    """
    critical_flow = observed_flow / S_i
    return critical_flow


def get_green_phases(tls_id):
    """
    Obtém o número de fases verdes de um semáforo, assumindo que as fases são organizadas
    como pares (verde seguido de transição: amarelo/vermelho).

    Args:
        tls_id (str): ID do semáforo no SUMO.

    Returns:
        int: Número de fases verdes no ciclo do semáforo (total de fases dividido por 2).
    """
    temp = traci.trafficlight.getAllProgramLogics(tls_id)
    temp = temp[0].phases
    num_phases = int(len(temp) / 2)
    return num_phases


def update_green_phases_manually(traffic_light_id, green_durations, lost_time=2):
    """
    Atualiza manualmente as fases de um semáforo no SUMO, atribuindo novas durações
    para as fases com luz verde e uma duração fixa para fases intermediárias (amarelas/vermelhas).

    Args:
        traffic_light_id (str): ID do semáforo no SUMO.
        green_durations (list[int]): Lista com as novas durações (em segundos) das fases verdes.
        lost_time (int, optional): Duração padrão para fases que não têm verde (transições). Padrão: 2 segundos.

    Returns:
        None
    """
    old_programs = traci.trafficlight.getAllProgramLogics(traffic_light_id)

    if len(old_programs) == 0:
        print(f"Nenhum programa encontrado para o semáforo '{traffic_light_id}'")
        return

    old_logic = old_programs[0]
    old_phases_raw = old_logic.phases

    novas_fases = []
    index_verde = 0

    for phase in old_phases_raw:
        if 'G' in phase.state:
            duracao = green_durations[index_verde] if index_verde < len(green_durations) else phase.duration
            index_verde += 1
        else:
            duracao = lost_time

        novas_fases.append(traci.trafficlight.Phase(duracao, phase.state))

    nova_logica = traci.trafficlight.Logic(
        programID=old_logic.programID,
        type=old_logic.type,
        currentPhaseIndex=0,
        phases=novas_fases
    )

    traci.trafficlight.setProgramLogic(traffic_light_id, nova_logica)
    print(f"Fases do semáforo '{traffic_light_id}' atualizadas com sucesso.")

def notification_agent(critical_flow_total):
    messages = {
        0.25: 'Sem Engarrafamento',
        0.5: 'Normal',
        0.75: 'Congestionado',
        float('inf'): 'Muito Congestionado'
    }
    for limit, message in messages.items():
        if critical_flow_total <= limit:
            return message
    
def get_tls_states(tlsID):
    current_phase_index = traci.trafficlight.getPhase(tlsID)
    program = traci.trafficlight.getAllProgramLogics(tlsID)[0]
    current_state = program.phases[current_phase_index].state
    return current_state