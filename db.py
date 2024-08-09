from flask_bcrypt import Bcrypt
import psycopg2
from app import app

app.config['SECRET_KEY'] = "c7bb9002b1c215c9f37e6f741c122c11"

bcrypt = Bcrypt(app)

# Function to establish database connection
def db_conn():
    DB_NAME = "pujanpaney"
    DB_USER = "pujanpaney_user"
    DB_PASS = "EsA2GJyO3OvR56JwcHpUBnkNcri4Wp5P"
    DB_HOST = "dpg-cqqr4p0gph6c738elvm0-a.oregon-postgres.render.com"
    DB_PORT = "5432"

    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    return conn

conn = db_conn()
cur = conn.cursor()
password1='1717-pujaN'
password2='2857-sauD'
hashed_password1 = bcrypt.generate_password_hash(password1).decode('utf-8')
hashed_password2 = bcrypt.generate_password_hash(password2).decode('utf-8')


#     CREATE TABLE customers (
#         customer_id SERIAL PRIMARY KEY,
#         name VARCHAR(255),
#         email VARCHAR(255),
#         phone_no VARCHAR(255),
#         password VARCHAR(255)
#     );

#     CREATE TABLE products (
#         product_id SERIAL PRIMARY KEY,
#         name VARCHAR(255),
#         price NUMERIC,
#         description VARCHAR(255),
#         photo VARCHAR(255),
#         quantity INTEGER
#     );

#     CREATE TABLE product_list (
#         list_id SERIAL PRIMARY KEY,
#         product_id INTEGER REFERENCES products(product_id),
#         quantity INTEGER,
#         customer_id INTEGER REFERENCES customers(customer_id)
#     );

#     CREATE TABLE orders (
#         order_id SERIAL PRIMARY KEY,
#         customer_id INTEGER REFERENCES customers(customer_id),
#         order_date DATE,
#         total_amount NUMERIC
#     );

#     CREATE TABLE reviews (
#         review_id SERIAL PRIMARY KEY,
#         product_id INTEGER REFERENCES products(product_id),
#         customer_id INTEGER REFERENCES customers(customer_id),
#         rating INTEGER,
#         comment TEXT
#     );

#     CREATE TABLE order_line (
#         order_list_id SERIAL PRIMARY KEY,
#         order_id INTEGER REFERENCES orders(order_id),
#         product_id INTEGER REFERENCES products(product_id),
#         quantity INTEGER,
#         price_at_order NUMERIC
#     );

#     CREATE TABLE admins (
#         admin_name VARCHAR(255),
#         admin_email VARCHAR(255),
#         admin_password VARCHAR(255)
#     );
   
cur.execute("insert into admins (admin_name,admin_email,admin_password) values (%s,%s,%s)",('Roshan singh saud','roshansinghsaud2001@gmail.com',hashed_password2))

conn.commit()
cur.close()
conn.close()
