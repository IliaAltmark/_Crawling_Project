import pymysql

from main_code.utils.utils import get_logger
from main_code.config.config import LOCAL_USER as LU, LOCAL_PASSWORD as LP


logger = get_logger(__name__)
LOCAL_USER = LU
LOCAL_PASSWORD = LP

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


def autoinc_uniques_insertion(connection, table_name, pk_name, data_column_name, data):
    """
        Add the given data to table named table_name, in the given connection's database.
        :param data: 
        :param data_column_name: 
        :param pk_name: 
        :param table_name:
        :param connection: a connection object to an sql server.
        """
    items_ids = []
    for it in data:
        command = f"""SELECT {pk_name} 
                            FROM {table_name}
                            WHERE {data_column_name}='{it}'
                          ;"""
        item_ids = sql_run(connection, command)

        if len(item_ids) == 0:
            command_insert = f"""INSERT INTO 
                                      {table_name} (
                                          {data_column_name}
                                      ) VALUES (
                                          '{it}'
                                      );"""
            id_value_query = "SELECT LAST_INSERT_ID();"
            sql_run(connection, command_insert)
            item_id = sql_run(connection, id_value_query)[0]['LAST_INSERT_ID()']
        else:
            item_id = item_ids[0][pk_name]
        items_ids.append(item_id)
    return items_ids
