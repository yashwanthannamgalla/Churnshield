from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import offers
import joblib




data=pd.read_csv("customer_dataset.csv")

x=data.drop(["customer_id","customer_name","churn"],axis=1)
y=data["churn"]

train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=0.2,random_state=15)

model= LogisticRegression( max_iter=2000
    )

#training
model.fit(train_x,train_y)

#predicting
predict=model.predict(test_x)
predicted =model.predict_proba(test_x)
churn_pred=predicted[:,1]

result= test_x.copy()
result["churn_probability"]=churn_pred

#print(result.head(100))


#accuracy 
acc=accuracy_score(test_y,predict)
tr_pred=model.predict(train_x)
tr_acc=accuracy_score(train_y,tr_pred)

print(acc,tr_acc)



joblib.dump(model, "churn_model.pkl")
print("Model saved")
