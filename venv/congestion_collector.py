import traci  # Importa a biblioteca TraCI para interagir com o SUMO
import json  # Importa JSON para carregar configurações
import traffic_utils  # Importa funções auxiliares do módulo traffic_utils

import mysql.connector  # Importa a biblioteca para conectar ao banco de dados MySQL

def run():
    # Carrega as configurações do SUMO a partir de um arquivo JSON
    with open("config_sumo.json", "r") as sumo_file:
        config = json.load(sumo_file)

    # Carrega as configurações do banco de dados a partir de um arquivo JSON
    with open("config_db.json", "r") as db_file:
        db_config = json.load(db_file)

    # Configuração dos parâmetros do SUMO
    Sumo_config = [
        config["sumo_binary"],  # Caminho para o binário do SUMO
        '-c', config["config_file"],  # Arquivo de configuração do SUMO
        '--step-length', config["step_length"],  # Define o tempo de cada passo da simulação
        '--delay', config["delay"],  # Define o atraso na execução
        '--lateral-resolution', config["delay"]  # Define a resolução lateral
    ]

    # Conecta ao banco de dados MySQL usando as credenciais carregadas
    cnx = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

    cur = cnx.cursor()  # Cria um cursor para executar comandos SQL

    # Query para inserir dados na tabela de estado de congestionamento
    query = """
        INSERT INTO my_db.congestion_state 
        (cycle_number, num_phases, phase_index, edge_id, observed_flow, critical_flow, critical_flow_total) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Início da execução principal do código
    
    traci.start(Sumo_config)  # Inicia a simulação do SUMO com os parâmetros configurados

    # Nome do semáforo a ser monitorado
    myTl = "Tl1"

    # Verifica se o semáforo está na lista de IDs do SUMO
    if myTl not in traci.trafficlight.getIDList():
        print(f"Erro: Semáforo '{myTl}' não encontrado.")  # Mensagem de erro se não encontrado
        traci.close()  # Fecha a conexão com o SUMO
        cnx.close()  # Fecha a conexão com o banco de dados
        exit()  # Encerra o programa

    # Variáveis para controle do ciclo dos semáforos
    cycle_number = 0  # Número do ciclo atual
    current_phase_index = 0  # Índice da fase do semáforo
    phase_start_time = traci.simulation.getTime()  # Obtém o tempo inicial da fase atual

    # Obtém a lista de detectores de indução presentes no cenário do SUMO
    detectors = traci.inductionloop.getIDList()

    # Se nenhum detector for encontrado, exibe um aviso
    if not detectors:
        print("Nenhum detector encontrado! Verifique sua configuração no SUMO.")

    # Obtém as fases do semáforo e filtra apenas as fases verdes
    phases = traci.trafficlight.getAllProgramLogics(myTl)[0].phases
    green_phases = [i for i, phase in enumerate(phases) if "G" in phase.state]
    numPhases = traffic_utils.get_green_phases(myTl)  # Obtém o número de fases verdes do semáforo
    print(f"{numPhases}\n")  # Exibe o número de fases verdes

    # Lista de edges associadas aos detectores
    edges = []
    for detector in detectors:
        lane_id = traci.inductionloop.getLaneID(detector)  # Obtém a lane associada ao detector
        edges.append(lane_id.split("_")[0])  # Extrai a edge da lane e adiciona à lista

    # Inicializa um dicionário para armazenar a contagem de veículos por edge
    detector_counts = {edg: 0 for edg in edges}

    # Loop principal da simulação: continua enquanto houver veículos previstos na simulação
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()  # Avança um passo na simulação
        step = traci.simulation.getTime()  # Obtém o tempo atual da simulação

        # Atualiza a contagem de veículos detectados
        update = traffic_utils.update_detector_counts(detectors)

        # Obtém a fase atual do semáforo
        current_phase = traci.trafficlight.getPhase(myTl)

        # Se a fase atual for uma fase verde
        if current_phase in green_phases:
            phase_duration = phases[current_phase].duration  # Obtém a duração da fase atual

            # Atualiza os detectores com base na fase atual
            update = traffic_utils.update_detector_counts(detectors, detector_counts)

            # Se a duração da fase verde terminou
            if step >= phase_start_time + phase_duration:
                print(f"\n🚦 Fim do Verde da Fase {current_phase} no Ciclo {cycle_number}")                    

                # Calcula os fluxos críticos baseados na contagem de veículos
                critical_flows = traffic_utils.calculate_critical_flow(detector_counts)
                critical_flow_total = sum(critical_flows.values())  # Soma dos fluxos críticos

                # Para cada edge, obtém os fluxos críticos e observados
                for edge, flow in critical_flows.items():
                    observed_flow = detector_counts.get(edge, 0)  # Obtém o fluxo observado

                    # Exibe os dados coletados
                    print(f"  - {edge}: Fluxo crítico = {flow:.4f} | Carros observados = {observed_flow}")

                    # Insere os dados no banco de dados
                    cur.execute(query, (cycle_number, numPhases, current_phase, edge, observed_flow, flow, critical_flow_total))

                cnx.commit()  # Confirma a transação no banco de dados

                # Resetar a contagem dos detectores para a próxima fase
                detector_counts = {edg: 0 for edg in edges}

                # Avançar para a próxima fase de verde
                current_phase_index = (current_phase_index + 1) % numPhases
                phase_start_time = step  # Atualiza o tempo de início da nova fase verde

                # Se todas as fases passaram, avança um ciclo
                if current_phase_index == 0:
                    cycle_number += 1
            
    traci.close()  # Finaliza a conexão com o SUMO
    cnx.close()  # Finaliza a conexão com o banco de dados

if __name__ == "__main__":
    run()