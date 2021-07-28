import pymysql

LOCAL_PASSWORD = None
LOCAL_USER = None


def establish_connection():
    """
    Establishes a connection to a local sql server.
    If the username and password haven't been initialized yet,
    asks the user to supply the messing information.
    :return a connection to the local sql server.
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


def sql_run(connection, mysql_statement, fields=None):
    """
    Runs the given sql command with the given connection.
    :param connection: a connection object to an sql server.
    :param mysql_statement: string of an sql statement.
    :param fields: fields for the execution of the statement.
    :return: the result of the sql request.
    """
    with connection.cursor() as cursor:
        # Read a single record
        if not fields:
            cursor.execute(mysql_statement)
        else:
            cursor.execute(mysql_statement, fields)
        connection.commit()
        return cursor.fetchall()


def close_connection(connection):
    """
    Closes the given connection to an sql server.
    :param connection: a connection to an sql server.
    :return:
    """
    connection.close()
    return "The connection is closed"
