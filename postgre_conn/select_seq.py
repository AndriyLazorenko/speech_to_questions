import psycopg2
from postgre_conn.config import config


TABLE_NAME = config(section='names')['table_name']


def get_transcripts_list():
    """
    Query all tuples from the words_seq table
    :return list of words sequences
    """
    sql_query = """
    SELECT duration_seconds, num_words, transcript, word_count FROM {0}
    """.format(TABLE_NAME)

    transcripts = list()

    def get_dict_list(transcripts):
        transcript_dict = dict()
        dict_list = list()
        for transcript in transcripts:
            transcript_dict['duration_seconds'], \
            transcript_dict['num_words'], \
            transcript_dict['transcript'], \
            transcript_dict['word_count'] \
                = transcript

            transcript_dict['duration_seconds'] = float(transcript_dict['duration_seconds'])

            dict_list.append(transcript_dict)
        return dict_list

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
            transcripts.append(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return get_dict_list(transcripts)


if __name__ == '__main__':
    print(get_transcripts_list())
