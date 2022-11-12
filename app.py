
import pandas as pd
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

#global vars
d={}
data = pd.read_excel("./data/dataset.xlsx")
# print(data)
d['price'] = list(data['preco'])[:20]
d['sales'] = list(data['venda'])[:20]
d['stock'] = list(data['estoque'])[:20]
unformatted_date = list(data['date'])[:20]
d['date'] = [i.strftime('%Y-%m-%d') for i in unformatted_date]


app = Flask(__name__)

#database connection
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rssia'
 
mysql = MySQL(app)


@app.route("/")
def home(): 

	# data = pd.read_excel("./data/dataset.xlsx")
	# # print(data)

	# price = list(data['preco'])[:20]
	# sales = list(data['venda'])[:20]
	# stock = list(data['estoque'])[:20]
	# unformatted_date = list(data['date'])[:20]
	# date = [i.strftime('%Y-%m-%d') for i in unformatted_date]
	
	# price=d["price"],sales=d["sales"],date=d["date"],stock=d["stock"]

	return render_template("graph.html",labelX='None',x_data=[],y_data=[])



@app.route("/",methods=["POST"])
def form_input():

	x = request.form['X-Value']
	y = request.form['Y-Value']
	
	if x=='' or y=='':
		return render_template("graph.html")

	labelX = str(x+"-"+y+" graph")

	return render_template("graph.html",x_data=d[x],y_data=d[y],x_name=x,y_name=y,labelX=labelX)


#login and registration 

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already ists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)






