import pandas as pd 

file=pd.read_csv("customer_dataset.csv")
print(file.columns)
print(file.sample(10))
