from flask import render_template,request,redirect,url_for,flash,Blueprint
from forms import insertproduct
import psycopg2


bac_bp = Blueprint('bac', __name__)
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


@bac_bp.route("/insertproducts",methods=['GET','POST'])
def insert():
    
    form = insertproduct()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description=form.description.data
        photo=form.photo.data

        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE name=%s ', (name,))
        user = cur.fetchone()

        if user:
            flash(f"The product {name} already exists", 'warning')
            cur.close()
            conn.close()
            return redirect(url_for('bac.insert'))

        cur.execute("INSERT INTO products (name, price, description, photo) VALUES (%s, %s, %s, %s)",
                    (name, price, description, photo))

        conn.commit()
        cur.close()
        conn.close()
        flash(f'New product {name} added successfully!', 'success')
        return redirect(url_for('crud'))

    return render_template('insert.html', form=form)  

def register_routes(app):
    app.register_blueprint(bac_bp)        
