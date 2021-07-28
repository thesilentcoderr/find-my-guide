from flask import Flask, render_template,request,json,url_for,session,flash,redirect
from flask_mysqldb import MySQL 
import os
from werkzeug.utils import  secure_filename
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
app.config['UPLOAD_FOLDER'] = var['upload_location']
app.secret_key = os.urandom(24)



@app.route("/")
def home():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM customer_blogs where img_link_1 != 'NULL' UNION ALL SELECT * FROM guides_blogs where img_link_1 != 'NULL' ORDER BY RAND ( );")
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
                return render_template('user_login.html', role='customer')
        else:
            cur.close()
            flash('User Does Not Exist!! Please Enter Valid Username.', 'danger')
            return render_template('user_login.html', role='customer')
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
        usercheck = cur.execute("SELECT * FROM customer;")
        if usercheck>0:
            users = cur.fetchall()
            print(users)
            for user in users:
                print(user)
                if (user[2] == email) or (user[3] == number):
                    flash("User Already Exists!, Please Login...")
                    return redirect('/user/customer_login')
        cur.execute("INSERT INTO customer (full_name,email_id,password,contact) values (%s,%s,%s,%s);", (name,email,password,number))
        mysql.connection.commit()
        cur.close()
        return redirect('/user/customer_login')

    return render_template("register_customer.html")

@app.route("/user/guide_register", methods=['GET', 'POST'])
def guide_register():
    if request.method == 'POST':
        form = request.form
        name = form['name'].split(' ',1)[0] 
        email = form['email']
        number = form['contact']
        city = form['city']
        gender = form['gender']
        english = form['english']
        price = form['price']
        password = gen(form['pass'])
        cur = mysql.connection.cursor()
        usercheck = cur.execute("SELECT * FROM guides;")
        if usercheck>0:
            users = cur.fetchall()
            print(users)
            for user in users:
                if (user[2] == email) or (user[3] == number):
                    flash("User Already Exists!, Please Login...")
                    return redirect('/user/guide_login')
        cur.execute("INSERT INTO guides(full_name,email_id , contact, city,gender,is_checked,price,password ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);", (name,email,number,city,gender,english,price,password))
        cur.execute("INSERT INTO rate_status (guide_id,rating) values (LAST_INSERT_ID(),NULL);")
        mysql.connection.commit()
        cur.close()
        return redirect('/user/guide_login')
    return render_template("register_guide.html")

@app.route("/booking/guides_blog/<int:id>/")
def guides_blog(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM guides_blogs WHERE blog_id={};".format(id))
        blog = cur.fetchone()
        return render_template('bloginfo.html',blog=blog)
    return redirect('/')

@app.route("/booking/customer_blog/<int:id>/")
def customer_blog(id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customer_blogs WHERE blog_id={}; ".format(id))
        blog = cur.fetchone()
        return render_template('bloginfo.html',blog=blog)
    return redirect('/')

@app.route("/booking")
def booking():
    if 'user' in session:
        cur = mysql.connection.cursor()
        if session['role'] == 'customer':
            q = cur.execute("select booking.*,customer_blogs.img_link_1,guides.full_name,ratings.rating,date,curdate()  from  customer_blogs,booking,guides,ratings where customer_blogs.blog_id=booking.booking_id and booking.guide_id=guides.id and ratings.booking_id=booking.booking_id and booking.customer_id={} ORDER BY booking_id DESC; ".format(session['id']))
        else:
            q = cur.execute("select booking.*,customer_blogs.img_link_1,guides.full_name,ratings.rating,curdate()  from  customer_blogs,booking,guides,ratings where customer_blogs.blog_id=booking.booking_id and booking.guide_id=guides.id and ratings.booking_id=booking.booking_id and booking.guide_id={} ORDER BY booking_id DESC; ".format(session['id']))
        if q>0:
            trips = cur.fetchall()
            return render_template("booking.html",trips=trips)
        else:
            return render_template("booking.html",trips=None)
    return redirect('/')

@app.route("/booking/end/<int:value>/")
def booking_end(value):
    if 'user' in session:
        value = str(value)
        booking_id = int(value[0])
        cur = mysql.connection.cursor()
        cur.execute("UPDATE booking SET status='Completed' where booking_id=%s;" ,([booking_id]))
        cur.execute("UPDATE guides SET status='A' where id=(SELECT guide_id from booking where booking_id={});".format(booking_id))
        return redirect('/customer_add_blog/{}'.format(booking_id))
    return redirect('/')

@app.route("/booking/cancel/<int:id>/")
def booking_cancel(id):
    if 'user' in  session:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE booking SET status='Cancelled' where booking_id={};".format(id))
        return redirect('/booking')
    return redirect('/')

@app.route("/booking/rate/<int:value>")
def guide_rate(value):
    if 'user' in session:
        value = str(value)
        booking_id = int(value[0])
        rating = int(value[1])
        guide_id = int(value[2])
        cur = mysql.connection.cursor()
        cur.execute("UPDATE ratings SET rating=%s WHERE booking_id=%s;",(rating,booking_id))
        cur.execute(" update rate_status set rating = (select avg(rating) from ratings where guide_id=%s) where guide_id=%s; ",(guide_id,guide_id))
        mysql.connection.commit()
        cur.close()
        return redirect('/booking/end/{}' .format(value))
    return redirect('/')

@app.route("/guides")
def guides():
    if 'user' in session:
        cur = mysql.connection.cursor()
        q = cur.execute("select guides.*, rate_status.rating from guides,rate_status where guides.id=rate_status.guide_id;")
        if q>0:
            guides=cur.fetchall()
            return render_template("display_guides.html",guides=guides)
        else:
            return render_template("display_guides.html",guides=None)
    return redirect('/')

@app.route("/book_guide/<int:id>/<name>/<city>", methods=['GET', 'POST'])
def book_guide(id,name,city):
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            trip_name = form['trip_title']
            city = city
            startDate = form['start_date']
            num_day = int(form['num_day'])-1
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO booking (trip_name,city,startDate,num_day,end_date,customer_id,guide_id) VALUES (%s,%s,%s,%s,ADDDATE(%s,%s),%s,%s);", (trip_name, city, startDate, num_day,startDate, num_day,session['id'],id))
            cur.execute(" INSERT INTO customer_blogs (blog_id,date,customer_id) VALUES (LAST_INSERT_ID(),%s,%s);",(startDate,session['id']))
            cur.execute(" INSERT INTO ratings(guide_id,booking_id) VALUES (%s,LAST_INSERT_ID());",([id]))
            cur.execute("UPDATE guides SET status='NA' where id={};".format(id))
            mysql.connection.commit()
            cur.close()
            return redirect('/booking')
        return render_template("new_trip.html",id=id,guide_name=name,city=city)
    return redirect('/')

@app.route("/customer_add_blog/<int:id>/", methods=['GET', 'POST'])
def customer_add_blog(id):
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            blog_id=id
            title=form['blog_title']
            description=form['blog_description']
            img_link_1=request.files['img_link_1']
            file_name = secure_filename(img_link_1.filename)
            img_link_1.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name ))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE customer_blogs SET title=%s, description=%s, img_link_1=%s WHERE blog_id=%s;",(title,description,file_name,blog_id))
            mysql.connection.commit()
            cur.close()
            return redirect('/booking')
        return render_template('add_blog.html',id=id)
    return redirect('/')

@app.route("/guide_add_blog/<int:blog_id>", methods=['GET', 'POST'])
def guide_add_blog(blod_id):
    if 'user' in session:
        if request.method == 'POST':
            blog_id=blod_id
            form = request.form
            title=form['blog_title']
            description=form['blog_description']
            img_link_1= form['img_link_1']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO guides_blogs(blog_id,title,description,img_link_1,guide_id) VALUES (%s,%s,%s,%s,%s);", (blog_id, title, description,img_link_1,session['id']))
            mysql.connection.commit()
            cur.close()
        return render_template('add_blog.html')
    return redirect('/')

@app.route("/logout")
def logout():
    if 'user' in session:
        session['logged_in'] = False
        session.pop('user') 
        session.pop('full_name') 
        session.pop('id') 
        session.pop('role') 
        flash('User Logged Out','success')
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=False)