import traci  # Importa a biblioteca TraCI para interagir com o SUMO
import json  # Importa JSON para carregar configurações
import traffic_utils

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
        '--lateral-resolution', config["lateral_resolution"]  # Define a resolução lateral
    ]

    # Conecta ao banco de dados MySQL usando as credenciais carregadas
    cnx = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

    database=db_config["database"]
    table_congestion_data = db_config["table_congestion_data"]
    table_notifications = db_config["table_notification"]
    table_states = db_config["table_states"]

    cur = cnx.cursor()  # Cria um cursor para executar comandos SQL

    # Query para inserir dados na tabela de estado de congestionamento

    query_congestionData_replace = f"""
        REPLACE INTO {database}.{table_congestion_data}
        (ID, Cycle_Number, Num_Phases, Phase_Index, Observed_Flow, Critical_Flow, Critical_Flow_TOTAL)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    query_notification_replace = f"""
        REPLACE INTO {database}.{table_notifications}
        (ID, Message)
        VALUES (%s, %s)
    """

    query_states_replace = f"""
        REPLACE INTO {database}.{table_states}
        (ID, States)
        VALUES (%s, %s)
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
    last_phase = 0
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

    observed_flow = 0
    phase_data = []
    # Loop principal da simulação: continua enquanto houver veículos previstos na simulação
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()  # Avança um passo na simulação
        step = traci.simulation.getTime()  # Obtém o tempo atual da simulação

        # Obtém a fase atual do semáforo
        current_phase = traci.trafficlight.getPhase(myTl)

        if current_phase != last_phase:
            previous_state = traffic_utils.get_tls_states(myTl)
            cur.execute(query_states_replace, (1, previous_state))
            cnx.commit()              

            last_phase = current_phase
            print("Estados inseridos\n")

        # Se a fase atual for uma fase verde
        if current_phase in green_phases:
            phase_duration = phases[current_phase].duration  # Obtém a duração da fase atual

            # Atualiza os detectores com base na fase atual
            observed_flow = traffic_utils.update_detector_counts(detectors,observed_flow)

            # Se a duração da fase verde terminou
            if step >= phase_start_time + phase_duration:                 

                # Calcula os fluxos críticos baseados na contagem de veículos
                flow = traffic_utils.calculate_critical_flow(observed_flow)

                print(f"\n Fim da Fase {current_phase} no Ciclo {cycle_number}")
                print(f"Fluxo crítico desta fase = {flow:.4f} | Carros observados = {observed_flow}")

                state = traffic_utils.get_tls_states(myTl)

                phase_data.append({
                    "cycle": cycle_number,
                    "phase": current_phase,
                    "observed_flow": observed_flow,
                    "critical_flow": flow
                })

                # Avançar para a próxima fase de verde
                current_phase_index = (current_phase_index + 1) % numPhases
                phase_start_time = step  # Atualiza o tempo de início da nova fase verde
                observed_flow = 0

                if current_phase_index == 0:
                    critical_flow_total = sum(p["critical_flow"] for p in phase_data)
                    print(f"Fluxo crítico total = {critical_flow_total:.4f} \nFim do Ciclo {cycle_number}\n")
                    massage = (traffic_utils.notification_agent(critical_flow_total),)
                    

                    # Substitui os dados no banco de dados
                    i = 0
                    for i, data in enumerate(phase_data):
                        cur.execute(query_congestionData_replace, (
                            i + 1,
                            data["cycle"],
                            numPhases,
                            data["phase"],
                            data["observed_flow"],
                            data["critical_flow"],
                            critical_flow_total
                        ))

                    cur.execute(query_notification_replace, (1, massage[0]))                           
                    cnx.commit()  # Confirma a transação no banco de dados
                    print("DADOS INSERIDOS\n")

                    phase_data = []
                    cycle_number += 1

    traci.close()  # Finaliza a conexão com o SUMO
    cnx.close()  # Finaliza a conexão com o banco de dados

if __name__ == "__main__":
    run()