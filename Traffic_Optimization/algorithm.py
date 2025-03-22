import mysql.connector as mc


min_green = 15
sf_default = 1800

class Trffclght:
    units = []

    def __init__(self,  n_phases : int, all_critcal_flow : float, of : list, sf : list, edges : list, all_red = 0, lst_phs_time = 2):
        if len(of) != n_phases:
            print("observed flows and number of phases do not match")
            exit(-1)

        self.units.append(self)                             #register the instance of trafficlight
        self.n_phases = n_phases                            #number of phases
        self.lost_time = (n_phases * lst_phs_time) + all_red#lost time
        self.observed_flows = of                                   #latest observed flows
        self.saturation_flows = sf                                  #total saturation flow on the routes
        self.critical_flows_rt = []
        for i in range(len(of)): self.critical_flows_rt.append(of[i] / sf[i])
        self.all_critical_flows_rt = all_critcal_flow          #summation of all critical flow
        self.optm_cycle = 0                             #latest cycle caulculated
        self.green_times = []                               #latest greens calculated
        self.edges = edges

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


def connect(connection_data: tuple):
    host, user, password, database = connection_data
    db = mc.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        auth_plugin='mysql_native_password'
        )

    return db


def fix_fetch(torto: list) -> list:
    fixed_list = []
    for i in torto:
        fixed_list.append(i[0])

    return fixed_list


def db_update(sinal : Trffclght, cursor, db):
    sql = "REPLACE INTO results (id, n_phases, optm_cycle, green_times, edges) VALUES (%s, %s, %s, %s, %s)"
    val = []
    for i in range(len(sinal.edges)):
        val.append(tuple((
            str(i + 1),
            str(sinal.n_phases),
            str(sinal.optm_cycle),
            str(sinal.green_times[i]),
            str(sinal.edges[i]))
        ))
    cursor.executemany(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")
def main():
    #initial setup
    connection_data = ("localhost", "root", "sapos123", "teste")
    db_gt = connect(connection_data)
    cursor_selector = db_gt.cursor(buffered=True)

    cursor_selector.execute("SELECT observed_flow FROM traffic_light")
    of = fix_fetch(cursor_selector.fetchall())
    #print(of)

    cursor_selector.execute("SELECT num_phases FROM traffic_light")
    n_phases = cursor_selector.fetchone()[0]
    #print(n_phases)

    cursor_selector.execute("SELECT critical_flow_total FROM traffic_light")
    all_crtclflw = cursor_selector.fetchone()[0]

    #defines the saturation flow list
    sf = [] #1800 default
    for i in range(len(of)):
        sf.append(sf_default)

    cursor_selector.execute("SELECT edge_id FROM traffic_light")
    edges = fix_fetch(cursor_selector.fetchall())
    #print(edges)

    #sets the trafficlight object
    sinal = Trffclght(n_phases, all_crtclflw, of, sf, edges, all_red = 12)
    sinal.update(all_crtclflw, of, sf)
    #print(sinal.optm_cycle)
    #print(sinal.green_times)

    cursor_selector.close()
    db_gt.close()

    # saving the data
    connection_data = ("localhost", "sapo", "1234", "traffic_results")
    db_in = connect(connection_data)
    cursor_in = db_in.cursor(buffered=True)

    db_update(sinal, cursor_in, db_in)

    cursor_in.close()
    db_in.close()


if __name__ == '__main__':
    main()
