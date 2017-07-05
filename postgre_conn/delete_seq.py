import psycopg2
from postgre_conn.config import config


def delete_seq(seq_id):
    """
    Delete seq by seq_id
    :return: number of deleted rows
    """
    sql_query = """
    DELETE FROM words_seq WHERE seq_id = %s
    """
    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # execute the DELETE statement
        cur.execute(sql_query, (seq_id,))
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
    deleted_rows = delete_seq(2)
    print('The number of deleted rows: ', deleted_rows)