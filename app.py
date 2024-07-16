from flask import Flask, render_template, redirect, url_for, flash, session, request
import psycopg2
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, loginform,adminloginform
from flask_session import Session
from bac import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = "c7bb9002b1c215c9f37e6f741c122c11"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
bcrypt = Bcrypt(app)
register_routes(app)

# Function to establish database connection
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

@app.route("/" , methods=['GET', 'POST'])
def hello_world():
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('select * from products where product_id =%s',(1,))
    mata=cur.fetchone()
    cur.execute('select * from products where product_id =%s',(2,))
    data=cur.fetchone()
    cur.execute('select * from products where product_id =%s',(3,))
    tata=cur.fetchone()
    return render_template('index.html',mata=mata,data=data,tata=tata)
     

@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm() 

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        phone_no = form.phone_no.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = db_conn()
        cur = conn.cursor()

        cur.execute('SELECT * FROM customers WHERE email=%s', (email,))
        user = cur.fetchone()

        if user:
            flash(f"The email {email} already exists", 'warning')
            cur.close()
            conn.close()
            return redirect(url_for('reg'))

        cur.execute('SELECT * FROM customers WHERE phone_no=%s', (phone_no,))
        buser = cur.fetchone()

        if buser:
            flash(f"The phone number {phone_no} already exists", 'warning')
            cur.close()
            conn.close()
            return redirect(url_for('reg'))

        cur.execute("INSERT INTO customers (name, email, phone_no, password) VALUES (%s, %s, %s, %s)",
                    (name, email, phone_no, hashed_password))

        conn.commit()
        cur.close()
        conn.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('reg'))

    return render_template('login.html', form=form)  

@app.route('/login', methods=['GET', 'POST'])
def login():
    bform = loginform()
    if bform.validate_on_submit():
        email = bform.email.data
        password = bform.password.data

        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers WHERE email=%s', (email,))
        cuser = cur.fetchone()
        cur.close()
        conn.close()

        if cuser:
            stored_hash = cuser[4]
            if bcrypt.check_password_hash(stored_hash, password):
                session["name"] = email
                flash("Logged in successfully!", 'success')
                return redirect(url_for('hello_world'))
            else:
                flash("Login failed. Check your email and password and try again.", 'danger')
        else:
            flash("Login failed. Check your email and password and try again.", 'danger')
        
    return render_template('alogin.html', bform=bform)

@app.route('/productinfo', methods=['GET', 'POST'])
def productinfo():
    if not session.get("name") and not session.get("email"):
        return redirect(url_for('login'))
    variable = request.args.get('var')
    conn= db_conn()
    cur= conn.cursor()
    cur.execute('select * from products where product_id =%s',(variable,))
    user=cur.fetchone()
    cur.close()
    return render_template('products.html',user=user)
     

    

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('name', None)
    session.pop('email', None)
    flash(f"Logged out successfully!", 'success')
    return redirect(url_for('hello_world'))
@app.route('/adminlogin',methods=['GET','POST'])
def admin():
    form=adminloginform()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        
        conn= db_conn()
        cur= conn.cursor()
        cur.execute('select * from admins where admin_email=%s and admin_name=%s',(email,name))
        user=cur.fetchone()
        cur.close()
        conn.close()

        if user:
          stored_hash=user[2]
          if bcrypt.check_password_hash(stored_hash, password):
              session["email"]=email
              flash("Logged in successfully!", 'success')
              return redirect(url_for('crud'))
          else:
                flash("Login failed. Check your email and password and try again.", 'danger')
        else:
            flash("Login failed. Check your email and password and try again.", 'danger')
        
    return render_template('admin.html', form=form)

@app.route('/adminpanel',methods=['GET','POST'])
def crud():
    if not session.get("email"):
        return redirect(url_for('login'))
    return render_template('adminpage.html')

              
        


if __name__ == "__main__":
    app.run(debug=True, port=8001)
