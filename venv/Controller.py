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


def has_data(cur, database: str) -> bool:
    sql = f"SELECT mode FROM {database}"
    cur.execute(sql)

    row = cur.fetchone()
    if row is not None:
        return True

    return False


def controller_flow(cur, db_config):

    table_auto = "traffic_updates"
    table_man = "traffic_updates_manual"

    '''if (counter % 10 == 0 and counter != 0):
        a = input("keep going?\n")
        if (a == "n"):
            cur.close()
            db_gt.close()
            traci.close()
            exit()'''

    if (not has_data(cur, table_man)):
        time.sleep(1)
        print("[CONTROLLER] No mode selected...")
        return


    sql = f"SELECT mode FROM {table_man}"
    cur.execute(sql)
    mode = cur.fetchone()[0]

    if mode == 1:
        database = table_man
        if (not has_data(cur, database)):
            print("[CONTROLLER] Manual mode: Waiting for order...")
            return

    else:
        database = table_auto
        time.sleep(1)
        if (not has_data(cur,  database)):
            print("[CONTROLLER] Automatic mode: Waiting for the data...")
            return

    # Busca os tempos otimizados
    sql = f"SELECT * FROM {database}"
    cur.execute(sql)
    row_data_raw = cur.fetchall()

    n_phases = int(row_data_raw[0][4])
    greens = []
    #cycle_time = row_data_raw[0][2]

    for i in range(n_phases):
        greens.append(row_data_raw[i][3])

        
    traffic_light_id = "Tl1"
    update_green_phases_manually(traffic_light_id, greens)


cnx = connect(
    "congestion-state.c02vqeowqrft.us-east-1.rds.amazonaws.com",
    "root",
    "bfgs2024",
    "congestion_state"
    )
cursor = cnx.cursor(buffered=True)
controller_flow(cursor, cnx)

cursor.close()
cnx.close()


