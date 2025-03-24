import time
import traci
import json
import mysql.connector as mc

file = "a"
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

def controller_flow(database, counter):
    db_gt = connect(
        "congestion-state.c02vqeowqrft.us-east-1.rds.amazonaws.com",
        "root",
        "bfgs2024",
        "congestion_state"
    )
    cursor_selector = db_gt.cursor(buffered=True)

    if (counter % 10 == 0 and counter != 0):
        a = input("keep going?\n")
        if (a == "n"):
            cursor_selector.close()
            db_gt.close()
            traci.close()
            exit()

    sql = f"SELECT mode FROM {database}"
    cursor_selector.execute(sql)
    if (cursor_selector.fetchone()[0] == 1):
        database = database_man
    if (cursor_selector.fetchone()[0] == 0):
        database = database_auto
    time.sleep(2)

    sql = f"SELECT * FROM {database}"
    cursor_selector.execute(sql)
    print(cursor_selector.rowcount, "record selected.")

    row_data_raw = cursor_selector.fetchall()
    print(row_data_raw)

    n_phases = int(row_data_raw[0][4])
    print(f'numero de fases {n_phases}')
    greens = []
    cycle_time = row_data_raw[0][2]
    for i in range(n_phases):
        greens.append(row_data_raw[i][3])
        print(greens[i])

    cursor_selector.close()
    db_gt.close()
    # update_green_phases_manually(traffic_light_id, greens)


def main():
    #traffic_light_id = traci.trafficlight.getIDList()[0]
    counter = 0
    database = database_auto

    while (True):
        controller_flow(database, counter)
        counter += 1



if __name__ == '__main__':
    main()
