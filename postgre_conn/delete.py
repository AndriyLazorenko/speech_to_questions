import psycopg2
from postgre_conn.config import config

TABLE_NAME = config(section='names')['table_name']


def delete_row(id):
    """
    Delete by id
    :return: number of deleted rows
    """
    sql_query = """
    DELETE FROM {0} WHERE id = {1}
    """.format(TABLE_NAME, id)

    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # execute the DELETE statement
        cur.execute(sql_query)
        # get the number of updated rows
        rows_deleted = cur.rowcount

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted

if __name__ == '__main__':
    print('The number of deleted rows: ', delete_row(2))