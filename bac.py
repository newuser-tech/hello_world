from flask import render_template,request,redirect,url_for,flash,Blueprint,session
from forms import insertproduct,deleteproduct
import psycopg2


bac_bp = Blueprint('bac', __name__)

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


@bac_bp.route("/insertproducts",methods=['GET','POST'])
def insert():

    
    form = insertproduct()
    if not session.get("email"):
        return redirect(url_for('admin'))
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        description=form.description.data
        photo=form.photo.data
        quantity=form.quantity.data

        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE name=%s and description=%s ', (name,description,))
        user = cur.fetchone()

        if user:
            cur.execute('update products set quantity=quantity+%s where name=%s',(quantity,name,))
            flash(f"The product {name} increased by {quantity} items", 'success')
            cur.close()
            conn.commit()
            conn.close()
            return redirect(url_for('bac.insert'))

        cur.execute("INSERT INTO products (name, price, description, photo,quantity) VALUES (%s, %s, %s, %s,%s)",
                    (name, price, description, photo,quantity))

        conn.commit()
        cur.close()
        conn.close()
        flash(f'New product {name} added successfully!', 'success')
        return redirect(url_for('crud'))

    return render_template('insert.html', form=form) 
@bac_bp.route('/add_to_cart', methods=['GET','POST']) 
def addtocart():
    values = request.args.get('value')

@bac_bp.route('/delete', methods=['GET','POST']) 
def delete():
    bform=deleteproduct()
    if not session.get("email"):
        return redirect(url_for('admin'))
    if bform.validate_on_submit():
        column=bform.column.data
        description=bform.description.data
        quan=bform.quan.data
        conn=db_conn()
        cur=conn.cursor()
        
        cur.execute('select * from products where name=%s',(column,))
        val=cur.fetchone()
        if val:
          cur.execute('select * from products where description=%s',(description,))
          vall=cur.fetchone()
          if vall:
              if vall[5]==0:
                cur.execute('delete from products where product_id=%s',(vall[0],))
                flash(f'item {vall[1]} deleted succesfully')
              else:
                  if vall[5] > quan:
                     cur.execute('update products set quantity=quantity-%s where product_id=%s',(quan,vall[0],))  
                     flash(f'{quan} {vall[1]} deleted successfully')
                  else:
                      flash(f"only {vall[5]} items remaining so you can't delete {quan} items")
                  
          else:
              flash('The description of item doesnot match','danger')
        else:
            flash(f'The column {column} doesnot exists') 
        cur.close()       
        conn.commit()
        conn.close()
           
    return render_template("delete.html",bform=bform)     





def register_routes(app):
    app.register_blueprint(bac_bp)        
