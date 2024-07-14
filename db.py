import psycopg2

def db_conn():
    DB_NAME = "hello"
    DB_USER = "postgres"
    DB_PASS = "computer@1234"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    return conn
conn=db_conn()
cur=conn.cursor()
cur.execute('delete from customers')
conn.commit()
cur.close()
conn.close()
