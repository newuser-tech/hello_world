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
# cur.execute('''create table customers(
#   customer_id serial primary key,
#   name varchar(255),
#   email varchar(255),
#   password varchar(255),
#   phone_no varchar(255)
# );

#   create table orders(
#   order_id integer primary key,
#   customer_id integer,
#   order_date date,
#   total_amount numeric);
            
#  create table products(
#   product_id serial primary key
#   name varchar(255),
#   price numeric
#   description varchar(255),
#    photo varchar(255),);
             
#   create table product_list(
#   product_id integer,
#   order_id integer,
#   quantity integer ,
#    foreign_key(product_id) references products(product_id) ,
#     foreign_key(order_id) references orders(order_id) ,                  
  
#    );  
#  create table orders(
#   product_id integer
#   product_id integer,
#   customer_id integer,
#   rating integer,
#   comment text,
#    foreign_key(product_id) references products(product_id) ,
#     foreign_key(customer_id) references customers(customer_id)                 
#                 );
            
#  create table admins(
#    admin_name varchar(255),
#    admin_email varchar(255),
#    admin_password varchar(255)  )           ''') 
cur.execute('alter table products add column quantity integer')
  
conn.commit()
cur.close()
conn.close()
