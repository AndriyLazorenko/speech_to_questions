import psycopg2
from postgre_conn.config import config


def insert_sequences(seq):
    """
    Insert sequences into the words_seq table
    """
    sql_query = """
        INSERT INTO words_seq(seq) VALUES(%s)
        RETURNING seq_id;
    """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql_query, (seq,))

        # get the generated id back
        seq_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()

        print('Added row with seq_id = {} '.format(seq_id))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    test_seq = ['bla', 'bla-bla', 'bla-bla-bla']
    insert_sequences(test_seq)