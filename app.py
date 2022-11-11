
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home(): 

	data = pd.read_excel("./data/dataset.xlsx")
	# print(data)

	price = list(data['preco'])[:20]
	sales = list(data['venda'])[:20]
	stock = list(data['estoque'])[:20]
	date = list(data['date'])[:20]
	new_date = [i.strftime('%Y-%m-%d') for i in date]



	# plt.figure(figsize=(10,10))
	# plt.style.use('seaborn')
	# plt.scatter(x,y,marker="*",s=100,edgecolors="black",c="red")
	# plt.title("Excel sheet to Scatter Plot")
	# plt.show()

	return render_template("graph.html",price=price,sales=sales,date=new_date,stock=stock)
