import psycopg2
from postgre_conn.config import config


def create_tables():
    """
    Create tables in the PostgreSQL database
    """
    command = """
        CREATE TABLE words_seq (
            seq_id SERIAL PRIMARY KEY,
            seq VARCHAR(255)[] NOT NULL
        )
        """
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # create table
        cur.execute(command)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()

        print('Table words_seq has been created')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()