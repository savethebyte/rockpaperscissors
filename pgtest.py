#!/usr/bin/python3

from os import getenv

from psycopg2 import OperationalError
from psycopg2.pool import SimpleConnectionPool
from secrets import pgpass

# TODO(developer): specify SQL connection details
CONNECTION_NAME = getenv(
  'INSTANCE_CONNECTION_NAME',
  'the-dominion-245004:us-central1:rps-db')
DB_USER = getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = getenv('POSTGRES_PASSWORD', pgpass)
DB_NAME = getenv('POSTGRES_DATABASE', 'postgres')

pg_config = {
  'user': DB_USER,
  'password': DB_PASSWORD,
  'dbname': DB_NAME
}

# Connection pools reuse connections between invocations,
# and handle dropped or expired connections automatically.
pg_pool = None

def __connect(host):
    """
    Helper function to connect to Postgres
    """
    global pg_pool
    pg_config['host'] = '35.222.151.109'
    pg_pool = SimpleConnectionPool(1, 1, **pg_config)

def postgres_get(username):
    global pg_pool

    # Initialize the pool lazily, in case SQL access isn't needed for this
    # GCF instance. Doing so minimizes the number of active SQL connections,
    # which helps keep your GCF instances under SQL connection limits.
    if not pg_pool:
        try:
            __connect(f'/cloudsql/{CONNECTION_NAME}')
            #print(CONNECTION_NAME)
        except OperationalError:
            # If production settings fail, use local development ones
            __connect('localhost')

    # Remember to close SQL resources declared while running this function.
    # Keep any declared in global scope (e.g. pg_pool) for later reuse.
    with pg_pool.getconn() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, lose , win, tie from rps WHERE "username" = \'%s\'''' % username)
        results = cursor.fetchone()
        pg_pool.putconn(conn)
        return results

def postgres_put(data):
    global pg_pool
    #print(data)
    sqlinsert = """INSERT INTO rps (username, password, lose, win, tie) 
                 VALUES ('{0}','{1}','{2}','{3}','{4}')"""
    sqlupdate = """UPDATE rps
                 SET win = win + %s,
                 lose = lose + %s,
                 tie = tie + %s
                 WHERE username = %s"""
    # Initialize the pool lazily, in case SQL access isn't needed for this
    # GCF instance. Doing so minimizes the number of active SQL connections,
    # which helps keep your GCF instances under SQL connection limits.
    if not pg_pool:
        try:
            __connect(f'/cloudsql/{CONNECTION_NAME}')
            #print(CONNECTION_NAME)
        except OperationalError:
            # If production settings fail, use local development ones
            __connect('localhost')

    # Remember to close SQL resources declared while running this function.
    # Keep any declared in global scope (e.g. pg_pool) for later reuse.
    with pg_pool.getconn() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, lose , win, tie from rps WHERE "username" = \'%s\'''' % data['user'])
        results = cursor.fetchone()
        if results is None:
            cursor.execute(sqlinsert.format(data['user'], 'password', str(data['lose']), str(data['win']), str(data['tie'])))
        cursor.execute(sqlupdate, (str(data['win']), str(data['lose']), str(data['tie']), data['user']))
        conn.commit()
        pg_pool.putconn(conn)