from flask import *

import mysql.connector

main = Flask(__name__, static_folder='static')

main.config['MYSQL_HOST'] = 'localhost'
main.config['MYSQL_USER'] = 'root'
main.config['MYSQL_PASSWORD'] = ''
main.config['MYSQL_DB'] = 'harish'
def connect_to_database():
    return mysql.connector.connect(
        host=main.config['MYSQL_HOST'],
        user=main.config['MYSQL_USER'],
        password=main.config['MYSQL_PASSWORD'],
        database=main.config['MYSQL_DB']
    )





@main.route('/')
def home():
    return render_template('base.html')

@main.route('/search')
def search():
    if request.method=='POST':
        starting=request.form['starting']
        destination=request.form['destination']

        conn = connect_to_database()
        cursor=conn.cursor()

        sql="SELECT buses FROM search WHERE starting = %s AND destination = %s"
        cursor.execute(sql,(starting,destination))
        search=cursor.fetchone()
        if search:
            return render_template('bus.html')
            
        else:
            return redirect('nobus')

    return render_template('search.html')


@main.route('/nobus')
def nobus():
    return 'No Buses are Available'


@main.route('/signin')
def signin():
    return render_template('signin.html') 


@main.route('/signin',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password=request.form['password']
        conn = connect_to_database()

            
        cursor = conn.cursor()
        sql = "INSERT INTO signin (username, email, phone, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, email, phone, password))

            
        conn.commit()
    
    return render_template('search.html')


@main.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        conn = connect_to_database()
        cursor = conn.cursor()

        
        sql = "SELECT * FROM signin WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        login = cursor.fetchone()

        if login:
            
            return render_template('search.html')
        else:
            error = "Invalid email or password. Please try again."
            return render_template('login.html', error=error)
        
    return render_template('login.html')




@main.route('/bus',methods=['GET','POST'])
def eagle():
    if request.method=='POST':
        starting=request.form['starting']
        destination=request.form['destination']
        conn = connect_to_database()
        cursor = conn.cursor()

        
        sql = "SELECT *FROM search "
        cursor.execute(sql)
        bus= cursor.fetchall()
        print(bus)
        return render_template('bus.html',bus=bus)

    return 'invalid request'

@main.route('/book',methods=['GET','POST'])
def book():
    if request.method=='POST':
        Username=request.form['username']
        Phone=request.form['phone']
        starting=request.form['starting']
        destination=request.form['destination']
        conn = connect_to_database()
        cursor=conn.cursor()
        sql = "INSERT INTO book (Username, Phone, `starting`, `destination`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (Username, Phone, starting, destination))


        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/success')
    
    return render_template('book.html')

@main.route('/success')
def success():
    return "<h1>Booking successful! Thank you</h1>."


if __name__=="__main__":
    main.run(debug=True)