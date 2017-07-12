import psycopg2
from postgre_conn.config import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_NAME = config()['database']


def create_db():
    """
    Create new database
    """
    command = """
        CREATE DATABASE {0}
        """.format(DATABASE_NAME)
    conn = None
    try:
        # read the connection parameters
        params = config(section='postgresql_newdb')
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # create db
        cur.execute(command)

        # close communication with the database server
        cur.close()
        # commit the changes
        conn.commit()

        print('DB has been created')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_db()