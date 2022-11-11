
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("./data/dataset.xlsx")
date = list(data['date'])[:10]

new_date = [i.strftime('%Y-%m-%d') for i in date]

print(type(new_date[0]))
print(new_date)