import mysql.connector as mc

min_green = 15
sf_default = 1800


class Trffclght:
    units = []

    def __init__(self, n_phases : int, all_critcal_flow : float, of : list, sf : list, phases : list, all_red = 0, lst_phs_time = 2):
        if len(of) != n_phases:
            print("observed flows and number of phases do not match")
            exit(-1)

        self.units.append(self)                                     #register the instance of trafficlight
        self.n_phases = n_phases                                    #number of phases
        self.lost_time = (n_phases * lst_phs_time) + all_red        #lost time
        self.observed_flows = of                                    #latest observed flows
        self.saturation_flows = sf                                  #total saturation flow on the routes
        self.critical_flows_rt = []
        for i in range(len(of)): self.critical_flows_rt.append(of[i] / sf[i])
        self.all_critical_flows_rt = all_critcal_flow               #summation of all critical flow
        self.optm_cycle = 0                                         #latest cycle caulculated
        self.green_times = []                                       #latest greens calculated
        self.phases = phases

    def update(self, all_crtclflw, of, sf):
        self.observed_flows = of #latest observed flows
        self.saturation_flows = sf    #total saturation flow on the routes
        for i in range(len(of)) : self.critical_flows_rt[i]= of[i] / sf[i] #
        self.all_critical_flows_rt = all_crtclflw  #summation of all critical flow
        self.optm_cycle = get_optmcycle(self.all_critical_flows_rt, self.lost_time)
        self.green_times = get_greens(self.critical_flows_rt, self.all_critical_flows_rt, self.optm_cycle, self.lost_time)


def get_optmcycle(allcrtflws_rt, lost_time : int):
    optm_cycle = (1.5 * float(lost_time) + 5) / (1 - allcrtflws_rt)

    return optm_cycle


def get_greens(crtflws_rt, allcrtflws_rt, ltst_optmcycle, lost_time):
    greens = []
    green = 0
    for i in range(len(crtflws_rt)):
        green = (crtflws_rt[i] / allcrtflws_rt) * (ltst_optmcycle - lost_time)
        if green < min_green:
            greens.append(min_green)
            continue

        greens.append(green)

    return greens


def connect(host, user, password, database):

    db = mc.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )

    return db


def fix_fetch(torto: list) -> list:
    fixed_list = []
    for i in torto:
        fixed_list.append(i[0])

    return fixed_list


def db_clean(cursor, db, table : str):
    sql = f"DELETE FROM {table}"
    cursor.execute(sql)
    db.commit()
    print(cursor.rowcount, "record inserted'nt.")


def db_update(sinal: Trffclght, cursor, db, table: str):
    sql = f"INSERT INTO {table} (id, phase_id, cycle_time, green_time, light_state) VALUES (%s, %s, %s, %s, %s)"
    val = []
    for i in range(len(sinal.phases)):
        val.append(tuple((
            str(i + 1),
            str(i + 1),
            str(sinal.optm_cycle),
            str(sinal.green_times[i]),
            str(sinal.n_phases)
        )))
    cursor.executemany(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")

def main():
    #initial setup
    db_gt = connect(
        "congestion-state.c02vqeowqrft.us-east-1.rds.amazonaws.com",
        "root",
        "bfgs2024",
        "congestion_state"
        )
    cursor_selector = db_gt.cursor(buffered=True)

    cursor_selector.execute("SELECT Num_phases FROM congestion_data WHERE cycle_number = 7")
    num_phases = cursor_selector.fetchone()[0]

    all_critical_flow = 0
    observed_flow = []
    phases = []

    cursor_selector.execute("SELECT Phase_Index, Observed_Flow, Critical_Flow, Critical_Flow_TOTAL FROM congestion_data WHERE cycle_number = 7")
    data = cursor_selector.fetchall()
    for i in range(num_phases):
        phases.append(int(data[i][0]/2)+1)
        observed_flow.append(int(data[i][1]))
        all_critical_flow = data[0][3]


    #defines the saturation flow list
    sf = [] #1800 default
    for i in range(num_phases):
        sf.append(sf_default)

    #sets the trafficlight object
    sinal = Trffclght(num_phases, all_critical_flow, observed_flow, sf, phases)
    sinal.update(all_critical_flow, observed_flow, sf)

    cursor_selector.close()
    db_gt.close()

    # saving the data
    db_in = connect(
        "congestion-state.c02vqeowqrft.us-east-1.rds.amazonaws.com",
        "root",
        "bfgs2024",
        "congestion_state"
        )
    cursor_in = db_in.cursor(buffered=True)

    db_clean(cursor_in, db_in, "traffic_updates")

    db_update(sinal, cursor_in, db_in, "traffic_updates")

    cursor_in.close()
    db_in.close()


if __name__ == '__main__':
    main()
