import pymysql

LOCAL_PASSWORD = None
LOCAL_USER = None


def establish_connection():
    """

    """
    global LOCAL_USER
    global LOCAL_PASSWORD

    if LOCAL_USER is None:
        LOCAL_USER = input("Please insert your local sql server username:")
    if LOCAL_PASSWORD is None:
        LOCAL_PASSWORD = input("Please insert your local sql server password:")
    connection = pymysql.connect(host='localhost',
                                 user=LOCAL_USER,
                                 password=LOCAL_PASSWORD,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def sql_run(connection, mysql_statement):
    """

    """
    with connection.cursor() as cursor:
        # Read a single record
        cursor.execute(mysql_statement)
        connection.commit()
        return cursor.fetchall()


def close_connection(connection):
    connection.close()
    return "The connection is closed"
