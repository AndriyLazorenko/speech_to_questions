import psycopg2
from postgre_conn.config import config

TABLE_NAME = config(section='table_name')['table_name']


def create_tables():
    """
    Create tables in the database
    """
    command = """
        CREATE TABLE {0} (
            id SERIAL PRIMARY KEY,
            duration_seconds DECIMAL(7,2),
            num_words INTEGER,
            transcript TEXT,
            word_count JSON
        )
        """.format(TABLE_NAME)
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

        print('Table has been created')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()