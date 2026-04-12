import joblib
import pandas as pd
import offers

# load model
model = joblib.load("churn_model.pkl")

# load data
data = pd.read_csv("customer_dataset.csv")

X = data.drop(["customer_id","customer_name","churn"], axis=1)

# predict churn probability
predicted = model.predict_proba(X)

data["churn_probability"] = predicted[:,1]



#imp features
imp=model.coef_[0]

fet_imp=pd.Series(imp,index=X.columns)   

top=fet_imp.sort_values(ascending=False)
print(top.head())

top_fet=top.index[2]
print(top_fet)
fet= offers.choose_offer(top_fet)
print(fet)


#predicting
predict=model.predict(X)
predicted =model.predict_proba(X)
churn_pred=predicted[:,1]

result= X.copy()
result["churn_probability"]=churn_pred


# top risky customers
top20 = data.sort_values(
    by="churn_probability",
    ascending=False
).head(5)

print(top20[[
    "customer_id",
    "customer_name",
    "churn_probability"
]].to_string(index=False))
