
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

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

	data = pd.read_excel("./data/dataset.xlsx")


	x = request.form['X-Value']
	y = request.form['Y-Value']
	
	if x=='' or y=='':
		return render_template("graph.html")

	labelX = str(x+"-"+y+" graph")

	return render_template("graph.html",x_data=d[x],y_data=d[y],x_name=x,y_name=y,labelX=labelX)