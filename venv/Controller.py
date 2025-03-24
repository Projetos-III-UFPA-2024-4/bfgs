import time
import traci
import mysql.connector as mc

database_auto = "traffic_updates"
database_man = "traffic_updates_manual"

#initial setup
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


def connect(host, user, password, database):

    db = mc.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )

    return db

def controller_flow(cur, db_config, counter = None):

    table_auto = db_config["traffic_updates"]
    table_man = db_config["traffic_updates_manual"]

    '''if (counter % 10 == 0 and counter != 0):
        a = input("keep going?\n")
        if (a == "n"):
            cur.close()
            db_gt.close()
            traci.close()
            exit()'''

    sql = f"SELECT mode FROM {table_auto}"
    cur.execute(sql)
    mode = cur.fetchone()[0]
    print(f"mode {mode}")

    if (mode == 1):
        database = table_man

        while True:
            sql = f"SELECT mode FROM {database}"
            cur.execute(sql)
            row = cur.fetchone()
            if row is None:
                break
            print("[Controller] Modo manual ativo. Aguardando liberação...")
            time.sleep(2)

    else:#(mode == 0)
        database = table_auto

    # Busca os tempos otimizados
    sql = f"SELECT * FROM {database}"
    cur.execute(sql)
    row_data_raw = cur.fetchall()

    if not row_data_raw:
        print("[Controller] Nenhum dado de otimização encontrado.")
        return

    n_phases = int(row_data_raw[0][4])
    greens = []
    cycle_time = row_data_raw[0][2]

    for i in range(n_phases):
        greens.append(row_data_raw[i][3])
        
    traffic_light_id = "Tl1"
    update_green_phases_manually(traffic_light_id, greens)
