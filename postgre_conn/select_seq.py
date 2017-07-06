import psycopg2
from postgre_conn.config import config


def get_seq():
    """
    Query all tuples from the words_seq table
    :return list of words sequences
    """
    sql_query = """
    SELECT seq_id, seq FROM words_seq
    """
    words_seq = list()

    # create a generator that splits the database calls into a series of calls
    def iter_row(cursor, size=10):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # execute the SELECT statement
        cur.execute(sql_query)

        for row in iter_row(cur):
            words_seq.append(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return words_seq

if __name__ == '__main__':
    print(get_seq())