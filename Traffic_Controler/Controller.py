import mysql.connector as mc

#initial setup
def connect(host, user, password, database):

    db = mc.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )

    return db


def main():
    db_gt = connect(
        "congestion-state.c02vqeowqrft.us-east-1.rds.amazonaws.com",
        "root",
        "bfgs2024",
        "congestion_state"
    )
    cursor_selector = db_gt.cursor(buffered=True)

    database = "traffic_updates"
    sql = f"SELECT * FROM {database}"
    cursor_selector.execute(sql)
    print(cursor_selector.rowcount, "record selected.")
    row_data_raw = cursor_selector.fetchall()
    print(row_data_raw)
    n_phases = int(row_data_raw[0][4])
    print(f'numero de fases {n_phases}')
    row_data = []
    for i in range(n_phases):
        row_data.append({ "phase_number": row_data_raw[i][1], "green_time": row_data_raw[i][3], "cycle": row_data_raw[i][2]})

    for i in range(len(row_data)):
        print(row_data[i])

    cursor_selector.close()
    db_gt.close()


if __name__ == '__main__':
    main()
    