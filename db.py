from flask_bcrypt import Bcrypt
import psycopg2
from app import app

app.config['SECRET_KEY'] = "c7bb9002b1c215c9f37e6f741c122c11"

bcrypt = Bcrypt(app)

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
cur.execute('alter table products add column photo varchar(255)')
conn.commit()
cur.close()
conn.close()
