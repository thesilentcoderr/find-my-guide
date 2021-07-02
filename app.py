from flask import Flask, render_template,request,json,url_for,session,flash,redirect
from flask_mysqldb import MySQL 
from os import urandom
from werkzeug.security import generate_password_hash as gen, check_password_hash as check
import math

app = Flask(__name__)


with open('vars.json','r') as v:
    variable = json.load(v)
    
var = variable["variables"]
db_keeps = variable["sql_conf"]



mysql = MySQL(app)
# MySQL Configuration
app.config['MYSQL_HOST'] = db_keeps["mysql_host"]
app.config['MYSQL_USER'] = db_keeps["mysql_user"]
app.config['MYSQL_PASSWORD'] = db_keeps["mysql_password"]
app.config['MYSQL_DB'] = db_keeps["mysql_db"]
app.config['MYSQL_PORT'] = db_keeps['mysql_port']
app.secret_key = urandom(24)



@app.route("/")
def home():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM customer_blogs UNION ALL SELECT * FROM guides_blogs ORDER BY RAND ( );")
    if q > 0:
        posts = cur.fetchall()
        last = math.ceil(len(posts)/int(var["num_posts"]))
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        posts = posts[(page-1)*int(var["num_posts"]) : (page-1)*int(var["num_posts"]) + int(var["num_posts"])]

        if page==1:
            prev = "#!"
            next = "/?page=" + str(page+1)
            type_page = 'start'
        elif page==last:
            next = "#!"
            prev = "/?page=" + str(page-1)
            type_page = 'last'
        else:
            next = "/?page=" + str(page+1)
            prev = "/?page=" + str(page-1)
            type_page = 'mid'

        return render_template('index.html',var=var, posts=posts,prev=prev,next=next,type_page=type_page)
    else:
        return render_template('index.html',var=var, posts=None)
    

@app.route("/user/customer_login",methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        form = request.form
        email = form['email']
        password = form['pass']
        cur = mysql.connection.cursor()
        usercheck = cur.execute("SELECT * FROM customer WHERE email_id=%s;", ([email]))
        print(usercheck)
        if usercheck > 0:
            user = cur.fetchone()
            checker = check(user[-2], password)
            if checker:
                session['logged_in'] = True
                session['user'] = user[2]
                session['full_name'] = user[1]
                session['id'] = user[0]
                session['role'] = 'customer'
                flash(f"Welcome {session['full_name']}!! Your Login is Successful", 'success')
            else:
                cur.close()
                flash('Wrong Password!! Please Check Again.', 'danger')
                return render_template('user_login.html')
        else:
            cur.close()
            flash('User Does Not Exist!! Please Enter Valid Username.', 'danger')
            return render_template('user_login.html')
        cur.close()
        return redirect('/')
    return render_template("user_login.html", role='customer')

@app.route("/user/guide_login",methods=['GET', 'POST'])
def guide_login():
    if request.method == 'POST':
        form = request.form
        email = form['email']
        password = form['pass']
        cur = mysql.connection.cursor()
        usercheck = cur.execute("SELECT * FROM guides WHERE email_id=%s;", ([email]))
        if usercheck > 0:
            user = cur.fetchone()
            checker = check(user[-1], password)
            if checker:
                session['logged_in'] = True
                session['user'] = user[2]
                session['full_name'] = user[1]
                session['id'] = user[0]
                session['role'] = 'guide'
                flash(f"Welcome {session['full_name']}!! Your Login is Successful", 'success')
            else:
                cur.close()
                flash('Wrong Password!! Please Check Again.', 'danger')
                return render_template('user_login.html',role='guide')
        else:
            cur.close()
            flash('User Does Not Exist!! Please Enter Valid Username.', 'danger')
            return render_template('user_login.html',role='guide')
        cur.close()
        return redirect('/')
    return render_template("user_login.html", role='guide')

@app.route("/user/customer_register", methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        email = form['email']
        number = form['contact']
        password = gen(form['pass'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer (full_name,email_id,password,contact) values (%s,%s,%s,%s);", (name,email,password,number))
        mysql.connection.commit()
        cur.close()
        return redirect('/user/customer_login')
    return render_template("register_user.html")

@app.route("/guides_blog/<int:id>/")
def guides_blog(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM guides_blogs WHERE blog_id={};".format(id))
    blog = cur.fetchone()
    return render_template('bloginfo.html',blog=blog)

@app.route("/customer_blog/<int:id>/")
def customer_blog(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customer_blogs WHERE blog_id={}; ".format(id))
    blog = cur.fetchone()
    return render_template('bloginfo.html',blog=blog)

@app.route("/booking")
def booking():
    cur = mysql.connection.cursor()
    q = cur.execute("select booking.*,customer_blogs.img_link_1,guides.full_name,ratings.rating  from  customer_blogs,booking,guides,ratings where customer_blogs.blog_id=booking.booking_id and booking.guide_id=guides.id and ratings.booking_id=booking.booking_id and booking.customer_id={} ; ".format(session['id']))
    if q>0:
        trips = cur.fetchall()
    return render_template("booking.html",trips=trips)

@app.route("/booking/end/<int:id>/")
def booking_end(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE booking SET status='Completed' where booking_id={};".format(id))
    return redirect('/booking')

@app.route("/booking/cancel/<int:id>/")
def booking_cancel(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE booking SET status='Cancelled' where booking_id={};".format(id))
    return redirect('/booking')

@app.route("/logout")
def logout():
    session.pop('logged_in')
    flash('User Logged Out','success')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)