
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
d['price'] = list(data['preco'])
d['sales'] = list(data['venda'])
d['stock'] = list(data['estoque'])
unformatted_date = list(data['date'])
d['date'] = [i.strftime('%Y-%m-%d') for i in unformatted_date]

months={
	"Jan":'01',
	"Feb":'02',
	"Mar":'03',
	"Apr":'04',
	"May":'05',
	"Jun":'06',
	"Jul":'07',
	"Aug":'08',
	"Sep":'09',
	"Oct":'10',
	"Nov":'11',
	"Dec":'12'
}


# temp = d['date']
# print(temp[:40])
# print()
# req = [i for i in temp if i[5:7]==months['Jan'] and i[:4]=='2014' ]            # 8:10 for day    0:4 for year
# startIndex = temp.index(req[0])
# endIndex = temp.index(req[-1])

# print(startIndex,endIndex)

# print(d['sales'][startIndex:endIndex+1])


#Insights

most_sales_count = str(max(d['sales']))
most_sales_index = d['sales'].index(max(d['sales']))
most_sales_date = d['date'][most_sales_index]

least_sales_index = d['sales'].index(min(d['sales']))
least_sales_date = d['date'][least_sales_index]

most_stock_count = str(max(d['stock']))
most_stock_index = d['stock'].index(max(d['stock']))
most_stock_date = d['date'][most_stock_index]
 
avg_stock_price = round(sum(d['price'])/len(d['price']),2)



app = Flask(__name__)

#database connection
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rssia'
 
mysql = MySQL(app)



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
    session.pop('X',None)
    session.pop('Y',None)
    session.pop('XX',None)
    session.pop('YY',None)
    session.pop('XX_data',None)
    session.pop('YY_data',None)
    session.pop('YYY_data',None)
    session.pop('Mon_rev',None)
    
    
    
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
            msg = 'Account already exists !'
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
            return redirect(url_for('login'))

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



#Unwanted

@app.route("/dash")
def base():
	return render_template("dash.html")

labelX = 'Date-Sales graph (overall)'

#dashboard

@app.route("/")
def home():

    current_x = str(session.get('X'))
    current_y = str(session.get('Y'))

    print(current_x,"  ",current_y)

    if current_x!='None' or current_y!='None':
        return render_template("graph.html",labelX=labelX,x_data=d[current_x],y_data=d[current_y],x_name=current_x,y_name=current_y,most_sales=most_sales_date+" "+most_sales_count,least_sales=least_sales_date,most_stock=most_stock_date+" ("+most_stock_count+")",avg_price=avg_stock_price)

    else:
        return render_template("graph.html",labelX=labelX,x_data=d['date'],y_data=d['sales'],x_name='date',y_name='sales',most_sales=most_sales_date+" ("+most_sales_count+")",least_sales=least_sales_date,most_stock=most_stock_date+" ("+most_stock_count+")",avg_price=avg_stock_price)


@app.route("/",methods=["POST"])
def form_input():

    x = request.form['X-Value']
    y = request.form['Y-Value']
    
    session['X'] = x
    session['Y'] = y


    if x=='' or y=='':
        return render_template("graph.html")

    labelX = str(x+"-"+y+" graph")

    return render_template("graph.html",labelX=labelX,x_data=d[x],y_data=d[y],x_name=x,y_name=y,most_sales=most_sales_date+" ("+most_sales_count+")",least_sales=least_sales_date,most_stock=most_stock_date+" ("+most_stock_count+")",avg_price=avg_stock_price)



#Visualizations

@app.route("/visuals")
def visuals():

    current_xx = str(session.get('XX'))
    current_yy = str(session.get('YY'))

    current_xx_data = session.get('XX_data')
    current_yy_data = session.get('YY_data')
    current_yyy_data = session.get('YYY_data')
    current_mon_rev = session.get('Mon_rev')

    if current_xx!='None' or current_yy!='None':
        return render_template("visuals.html",xx_data=current_xx_data,yy_data=current_yy_data,xxx_data=current_xx_data,yyy_data=current_yyy_data,xx_name=current_xx,yy_name=current_yy,mon_rev=current_mon_rev)

    temp = d['date']
    req = [i for i in temp if i[5:7]=='01' and i[:4]=='2014' ]            # Default Jan 2014
    startIndex = temp.index(req[0])
    endIndex = temp.index(req[-1])

    halo = d['sales'][startIndex:endIndex+1]
    infinite = d['price'][startIndex:endIndex+1]

    mon_rev = 1
    for i in range(len(halo)):
        mon_rev +=  float(halo[i])*float(infinite[i])
    mon_rev = round(mon_rev,2)

    print(mon_rev)

    return render_template("visuals.html",xx_data=d['date'][startIndex:endIndex+1],yy_data=d['sales'][startIndex:endIndex+1],xxx_data=d['date'][startIndex:endIndex+1],yyy_data=d['stock'][startIndex:endIndex+1],xx_name='Jan',yy_name='2014',mon_rev=mon_rev)


@app.route("/visuals", methods =['GET', 'POST'])
def visuals_form():

    xx = request.form['Month']
    yy = request.form['Year']

    temp = d['date']
    req = [i for i in temp if i[5:7]==months[xx] and i[:4]==yy ]            # 8:10 for day    0:4 for year
    startIndex = temp.index(req[0])
    endIndex = temp.index(req[-1])

    halo = d['sales'][startIndex:endIndex+1]
    infinite = d['price'][startIndex:endIndex+1]

    mon_rev = 1
    for i in range(len(halo)):
        mon_rev +=  float(halo[i])*float(infinite[i])

    mon_rev = round(mon_rev,2)

    xx_data = d['date'][startIndex:endIndex+1]
    yy_data = d['sales'][startIndex:endIndex+1]
    yyy_data = d['stock'][startIndex:endIndex+1] 

    session['XX'] = xx
    session['YY'] = yy
    session['XX_data'] = xx_data
    session['YY_data'] = yy_data
    session['YYY_data'] = yyy_data
    session['Mon_rev'] = mon_rev


    return render_template("visuals.html",xx_data=xx_data,yy_data=yy_data,xxx_data=xx_data,yyy_data=yyy_data,xx_name=xx,yy_name=yy,mon_rev=mon_rev)

