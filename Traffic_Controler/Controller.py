import mysql.connector as mc

#initial setup
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


def main():
    connection_data = ("localhost", "root", "sapos123", "traffic_results")
    db_gt = connect(connection_data)
    cursor_selector = db_gt.cursor(buffered=True)

    cursor_selector.close()
    db_gt.close()


if __name__ == '__main__':
    main()