import sqlite3
from sqlite3 import Error
import base64


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


database = r"C:\sqlite\db\meter.db"

meter_table = """ CREATE TABLE IF NOT EXISTS meter (
                                    id integer PRIMARY KEY,
                                    mea_number text NOT NULL,
                                    customer_number text NOT NULL,
                                    ip_address text NOT NULL,
                                    password text NOT NULL
                                ); """

readmeter_table = """CREATE TABLE IF NOT EXISTS readmeter (
                                id integer PRIMARY KEY,
                                mea_number text NOT NULL,
                                Wh_total text NOT NULL,
                                Wh_on_peek text NOT NULL,
                                Wh_off_peek text NOT NULL,
                                version text NOT NULL,
                                reboot_interval text NOT NULL,
                                program_id integer NOT NULL
                            );"""

# create a database connection
conn = create_connection(database)
c = conn.cursor()

# create tables
if conn is not None:
    create_table(conn, meter_table)
    create_table(conn, readmeter_table)
else:
    print("Error! cannot create the database connection.")

# encode password
# password = '12345678'
# password_bytes = password.encode('ascii')
# base64_bytes = base64.b64encode(password_bytes)
# base64_message = base64_bytes.decode('ascii')

# decode password
# base64_message = 'MTIzNDU2Nzg='
# base64_bytes = base64_message.encode('ascii')
# password_bytes = base64.b64decode(base64_bytes)
# password = password_bytes.decode('ascii')

conn.commit()

# Closing the connection
conn.close()
