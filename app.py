from flask import Flask, render_template, redirect, url_for, flash, session, request
import psycopg2
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, loginform
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = "c7bb9002b1c215c9f37e6f741c122c11"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
bcrypt = Bcrypt(app)

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

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()  # Use form here

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

    return render_template('login.html', form=form)  # Use form here

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
                return redirect(url_for('productinfo'))
            else:
                flash("Login failed. Check your email and password and try again.", 'danger')
        else:
            flash("Login failed. Check your email and password and try again.", 'danger')
        
    return render_template('alogin.html', bform=bform)

@app.route('/productinfo', methods=['GET', 'POST'])
def productinfo():
    if not session.get("name"):
        return redirect(url_for('login'))
    return render_template('products.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('name', None)
    flash("Logged out successfully!", 'success')
    return redirect(url_for('hello_world'))

if __name__ == "__main__":
    app.run(debug=True, port=8001)
