import traci  # Importa a biblioteca TraCI para interagir com o SUMO
import json  # Importa JSON para carregar configurações
import mysql.connector  # Importa a biblioteca para conectar ao banco de dados MySQL

def get_useful_edges():
    """
    Retorna uma lista de edges úteis, removendo aquelas que pertencem a clusters internos do SUMO.
    
    Returns:
        list: Lista de IDs de edges filtradas (removendo clusters internos do SUMO).
    """
    edges_id = traci.edge.getIDList()  # Obtém todos os IDs de edges na simulação
    useful_edges_id = [edge for edge in edges_id if not edge.startswith(":cluster")]  # Filtra as edges úteis
    return useful_edges_id  # Retorna a lista de edges filtradas

def get_green_phases(tls_id):
    """
    Obtém o número de fases verdes do semáforo.

    Args:
        tls_id (str): ID do semáforo no SUMO.

    Returns:
        int: Número de fases verdes no ciclo do semáforo.
    """
    temp = traci.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)  # Obtém a definição completa do semáforo
    temp = temp[0].phases  # Acessa a primeira configuração do semáforo
    num_phases = int(len(temp) / 2)  # Divide por 2 para considerar apenas as fases verdes
    return num_phases  # Retorna o número de fases verdes

def update_detector_counts(detectors, detector_counts=None):
    """
    Atualiza e acumula a contagem de veículos para cada abordagem (edge) ao longo do ciclo do semáforo.

    Args:
        detectors (list): Lista de detectores de indução presentes na simulação.
        detector_counts (dict, opcional): Dicionário que mantém a contagem acumulada de veículos por abordagem. 
                                          Se None, um novo dicionário é criado.

    Returns:
        dict: Dicionário atualizado com a contagem acumulada de veículos por abordagem (edge).
    """
    if detector_counts is None:
        detector_counts = {}  # Garante que o dicionário não seja sobrescrito incorretamente entre chamadas

    for detector in detectors:
        lane_id = traci.inductionloop.getLaneID(detector)  # Obtém a lane associada ao detector
        count = traci.inductionloop.getLastStepVehicleNumber(detector)  # Obtém o número de veículos no detector

        approach = lane_id.split("_")[0]  # Obtém a aproximação (edge) baseada no nome da lane
        
        # Atualiza a contagem de veículos detectados por edge
        if approach in detector_counts:
            detector_counts[approach] += count  # Acumula veículos detectados na abordagem
        else:
            detector_counts[approach] = count  # Inicializa contagem caso seja a primeira vez

    return detector_counts  # Retorna o dicionário atualizado com a contagem de veículos por edge

def calculate_critical_flow(detector_counts, S_i=1800,):
    """
    Calcula o fluxo crítico com base nos veículos detectados no ciclo.

    Args:
        detector_counts (dict): Dicionário contendo a contagem de veículos por abordagem (edge).
        S_i (int, opcional): Capacidade de saturação padrão (veículos por hora), padrão de 1800 veículos/h.

    Returns:
        dict: Dicionário com o fluxo crítico calculado para cada abordagem (edge).
    """
    critical_flows = {}  # Inicializa o dicionário que armazenará os fluxos críticos

    for approach, count in detector_counts.items():    
        # Se a abordagem ainda não foi registrada, inicializa com o valor do fluxo calculado
        if approach not in critical_flows:
            critical_flows[approach] = count / S_i
        else:
            critical_flows[approach] = max(critical_flows[approach], count / S_i)  # Mantém o maior valor do fluxo crítico

    return critical_flows  # Retorna o dicionário contendo os fluxos críticos calculados para cada edge

def update_green_phases_manually(traffic_light_id, green_durations, lost_time = 2):
    """
    Atualiza as fases de um semáforo, mantendo os mesmos estados,
    definindo durações personalizadas apenas para fases com luz verde,
    e fixando as demais (ex: amarelas) com 2 segundos.

    Parâmetros:
    - traffic_light_id (str): ID do semáforo no SUMO
    - duracoes_verde (list[int]): Lista de durações desejadas para as fases com 'G'
    """

    old_programs = traci.trafficlight.getAllProgramLogics(traffic_light_id)

    if len(old_programs) == 0:
        print(f"⚠️ Nenhum programa encontrado para o semáforo '{traffic_light_id}'")
        return

    old_logic = old_programs[0]
    old_phases_raw = old_logic.phases

    novas_fases = []
    index_verde = 0

    for phase in old_phases_raw:
        if 'G' in phase.state:  # fase com verde
            duracao = green_durations[index_verde] if index_verde < len(green_durations) else phase.duration
            index_verde += 1
        else:  # fase de transição (amarelo ou vermelho total)
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