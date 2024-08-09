from flask import Flask, render_template, redirect, url_for, flash, session, request
import psycopg2
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, loginform,adminloginform,searchform,reviewsform,selectionform,quantityform
from flask_session import Session
from bac import register_routes
from psycopg2 import sql

app = Flask(__name__)
app.config['SECRET_KEY'] = "c7bb9002b1c215c9f37e6f741c122c11"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
bcrypt = Bcrypt(app)
register_routes(app)

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

@app.route("/" , methods=['GET', 'POST'])
def hello_world():
    conn=db_conn()
    cur=conn.cursor()
    search_results=[]
    form=searchform()
    bcr=form.var.data
    patt='%%'
    a=[]
    cur.execute('select * from products where name ilike %s',(patt,))
    a=cur.fetchall()
    if a:
      b=a[0][0]
    else:
        b=0
    
    cur.execute('select * from products where product_id =%s',(b,))
    mata=cur.fetchone()
    cur.execute('select * from products where product_id =%s',(b+1,))
    data=cur.fetchone()
    cur.execute('select * from products where product_id =%s',(b+2,))
    tata=cur.fetchone()
    cur.execute('select * from products where product_id =%s',(b+3,))
    aata=cur.fetchone()
    cur.execute('select * from products where product_id =%s',(b+4,))
    rata=cur.fetchone()
    cur.execute('select * from products where product_id =%s',(b+5,))
    lata=cur.fetchone()
    if bcr != '' :
       pattern = f'{bcr}%'
       cur.execute('SELECT * FROM products WHERE name ILIKE %s', (pattern,))

       search_results=cur.fetchall()
    
    else:
        flash("Please enter item you want to search:",'danger')   


    return render_template('index.html',mata=mata,data=data,tata=tata,result=search_results,form=form,bcr=bcr,aata=aata,lata=lata,rata=rata)
     

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
    if  session.get("email"):
        flash("already logged in as admin",'danger')
    
        return redirect(url_for('hello_world'))
        
    
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
    else:
        form = reviewsform()
        bform = quantityform()
        conn = db_conn()
        cur = conn.cursor()

        product_id = request.args.get('var') or request.args.get('val')
        user_email = session.get('name')
        quant = 0

        if not product_id:
            flash("Product ID not provided", "danger")
            return redirect(url_for('hello_world'))

        cur.execute('SELECT * FROM customers WHERE email = %s', (user_email,))
        customer = cur.fetchone()
        if customer is None:
            flash("Sorry, admin cannot enter this page", "danger")
            return redirect(url_for('hello_world'))

        customer_id = customer[3]

        # Fetch product details
        cur.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
        product = cur.fetchone()

        if not product:
            flash("Product not found", "danger")
            return redirect(url_for('hello_world'))

        # Fetch top 3 reviews for the product
        cur.execute('SELECT r.review_id, r.customer_id, r.product_id, r.rating, r.comment, c.name '
                    'FROM reviews r JOIN customers c ON r.customer_id = c.customer_id '
                    'WHERE r.product_id = %s '
                    'ORDER BY r.review_id LIMIT 3', (product_id,))
        reviews = cur.fetchall()

        avg_rating = 0
        if reviews:
            cur.execute('SELECT AVG(rating) FROM reviews WHERE product_id = %s', (product_id,))
            avg_rating = cur.fetchone()[0]

        if 'submit_review' in request.form and form.validate_on_submit() and session.get('name'):
            review = form.review.data
            rating = form.rating.data
            cur.execute('INSERT INTO reviews (product_id, customer_id, rating, comment) VALUES (%s, %s, %s, %s)',
                        (product_id, customer_id, rating, review))
            conn.commit()
            flash('Review submitted successfully', 'success')
            return redirect(url_for('productinfo', var=product_id))

        if bform.validate_on_submit():
            quant = bform.quant.data
           

    return render_template('products.html', user=product, form=form, reviews=reviews, avg=avg_rating, bform=bform, quant=quant)


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
        return redirect(url_for('admin'))
    return render_template('adminpage.html')


@app.route('/select', methods=['GET', 'POST'])
def select():
    form = selectionform()

    if form.validate_on_submit():
        table = form.table.data
        conn = db_conn()
        cur = conn.cursor()
        
        try:
            # Validate table name
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s", (table,))
            if not cur.fetchone():
                raise ValueError("Table does not exist")

            # Fetch data from the specified table and column names
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table))
            cur.execute(query)
            user = cur.fetchall()
            
            # Fetch column names
            columns = [desc[0] for desc in cur.description]
        except Exception as e:
            flash("Sorry! Table name does not exist in the database or an error occurred.", 'danger')
            user = []
            columns = []
        finally:
            cur.close()
            conn.close()

        return render_template('selection.html', form=form, columns=columns, user=user)
    return render_template('selection.html', form=form, columns=[], user=[])
@app.route('/addtocart', methods=['GET', 'POST'])
def add_to_cart():
    product_id = request.args.get('user')  # Should be the product ID
    quantity = int(request.args.get('quant'))  # Should be the quantity selected

    if not product_id or not quantity:
        flash('Invalid product or quantity.', 'danger')
        return redirect(url_for('hello_world'))

    conn = db_conn()
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM customers WHERE email=%s', (session.get('name'),))
        customer = cur.fetchone()

        if not customer:
            flash('User not found. Please log in again.', 'danger')
            return redirect(url_for('login'))

        customer_id = customer[3]

        cur.execute('SELECT * FROM products WHERE product_id=%s', (product_id,))
        product = cur.fetchone()

        if not product:
            flash('Product not found.', 'danger')
            return redirect(url_for('hello_world'))

        if product[5] >= quantity:
            cur.execute('INSERT INTO product_list(product_id, quantity, customer_id) VALUES (%s, %s, %s)',
                        (product_id, quantity, customer_id))
            cur.execute('UPDATE products SET quantity=quantity-%s WHERE product_id=%s',
                        (quantity, product_id))
            conn.commit()
            flash('Item added to your cart successfully', 'success')
        else:
            flash(f'Only {product[5]} items available. Please choose a lower quantity.', 'danger')

    except Exception as e:
        conn.rollback()
        flash(f'Error adding item to cart: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('your_cart'))
    

@app.route('/your_cart', methods=['GET', 'POST'])
def your_cart():
    if not session.get("name"):
        flash("Please log in to view your cart.", 'danger')
        return redirect(url_for('login'))

    conn = db_conn()
    cur = conn.cursor()

    cur.execute('SELECT * FROM customers WHERE email=%s', (session.get('name'),))
    customer = cur.fetchone()

    if not customer:
        flash("Customer not found.", 'danger')
        return redirect(url_for('hello_world'))

    customer_id = customer[3]
    customer_name = customer[0]

    cur.execute('''
        SELECT p.product_id, p.name, p.price, pl.quantity
        FROM product_list pl
        JOIN products p ON pl.product_id = p.product_id
        WHERE pl.customer_id = %s
    ''', (customer_id,))
    
    cart_items = cur.fetchall()
    total_amount = sum(item[2] * item[3] for item in cart_items)

    if request.method == 'POST':
        if cart_items:
            try:
                # Insert a new order and get the order ID
                cur.execute('''
                    INSERT INTO orders (customer_id, total_amount)
                    VALUES (%s, %s)
                    RETURNING order_id
                ''', (customer_id, total_amount))
                order_id = cur.fetchone()[0]
                
                # Insert each cart item into the order_line table
                for item in cart_items:
                    product_id = item[0]
                    price_at_order = item[2]
                    quantity = item[3]

                    cur.execute('''
                        INSERT INTO order_line (order_id, product_id, quantity, price_at_order)
                        VALUES (%s, %s, %s, %s)
                    ''', (order_id, product_id, quantity, price_at_order))

                # Clear the product_list table for this customer
                cur.execute('DELETE FROM product_list WHERE customer_id = %s', (customer_id,))

                conn.commit()
                flash("Order placed successfully!", 'success')

            except Exception as e:
                conn.rollback()
                flash(f"Error placing order: {str(e)}", 'danger')

        else:
            flash("Your cart is empty.", 'danger')

        cur.close()
        conn.close()
        return redirect(url_for('hello_world'))

    cur.close()
    conn.close()

    return render_template('display.html', customer_name=customer_name, cart_items=cart_items, total_amount=total_amount)


    return render_template('display.html', customer_name=customer_name, cart_items=cart_items, total_amount=total_amount)
@app.route('/vieworders', methods=['GET', 'POST'])
def vieworders():
    if not session.get("email"):  # Check if admin is logged in
        flash("Please log in as an admin to view orders.", 'danger')
        return redirect(url_for('admin'))

    conn = db_conn()
    cur = conn.cursor()

    # Fetch customer details, order details, and associated product details
    cur.execute('''
        SELECT c.name, c.phone_no, o.order_id, p.name as product_name, p.price, ol.quantity, (p.price * ol.quantity) as product_total
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_line ol ON o.order_id = ol.order_id
        JOIN products p ON ol.product_id = p.product_id
        ORDER BY o.order_id
    ''')

    orders = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('view.html', orders=orders)




if __name__ == "__main__":
    app.run()



              
        


