import psycopg2
from postgre_conn.config import config

import json

TABLE_NAME = config(section='names')['table_name']


def insert_all_transcripts(transcript_dict=dict()):
    for file in transcript_dict:
        insert_transcript(transcript_dict[file])


def insert_transcript(seq=dict()):
    """
    Insert one file from json into the table
    """

    def sql_query(transcript_dict):
        return """
            INSERT INTO {4} 
            (duration_seconds, num_words, transcript, word_count) 
            VALUES({0}, {1}, '{2}', '{3}')
            RETURNING id;
        """.format(transcript_dict['duration_seconds'],
                   transcript_dict['num_words'],
                   transcript_dict['transcript'],
                   json.dumps(transcript_dict['word_count']),
                   TABLE_NAME
                   )

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql_query(seq))

        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()

        print('Added row with id = {} '.format(id))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    test_seq = {"duration_seconds": 23.936, "word_count": {"\u0410\u0440\u0442\u0451\u043c": 1, "Daikin": 1, "\u0435\u0434\u0443": 1, "\u043d\u0430": 1, "\u0440\u0430\u0431\u043e\u0442\u0443": 2, "\u041d\u0430": 1, "\u0432\u044b\u0439\u0434\u0443": 1, "\u043a\u043e\u043d\u0435\u0447\u043d\u043e": 1, "\u0432": 3, "\u041e\u043c\u0441\u043a\u0435": 2, "\u0435\u0441\u0442\u044c": 1, "\u0440\u0435\u0431\u044f\u0442\u0430": 1, "\u043a\u043e\u0442\u043e\u0440\u044b\u0435": 1, "\u042f": 1, "\u041c\u043e\u0441\u043a\u0432\u0435": 1, "\u041d\u0443": 1, "\u043f\u043e\u043d\u044f\u043b": 1, "\u0425\u043e\u0440\u043e\u0448\u043e": 1, "\u0442\u043e\u0433\u0434\u0430": 1, "\u0436\u0434\u0443": 2}, "num_words": 25, "transcript": "\u0410\u0440\u0442\u0451\u043c Daikin \u0435\u0434\u0443 \u043d\u0430 \u0440\u0430\u0431\u043e\u0442\u0443 \u041d\u0430 \u0440\u0430\u0431\u043e\u0442\u0443 \u0432\u044b\u0439\u0434\u0443 \u043a\u043e\u043d\u0435\u0447\u043d\u043e \u0432 \u041e\u043c\u0441\u043a\u0435 \u0435\u0441\u0442\u044c \u0440\u0435\u0431\u044f\u0442\u0430 \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0432 \u041e\u043c\u0441\u043a\u0435 \u042f \u0432 \u041c\u043e\u0441\u043a\u0432\u0435 \u041d\u0443 \u043f\u043e\u043d\u044f\u043b \u0425\u043e\u0440\u043e\u0448\u043e \u0442\u043e\u0433\u0434\u0430 \u0436\u0434\u0443 \u0436\u0434\u0443"}
    insert_transcript(test_seq)