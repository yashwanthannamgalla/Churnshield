import pandas as pd
import numpy as np 

rows = 1000

names = ["Yashwanth","Vikram","ShivaPrasad","Jashwanth","muzammil","veer","hasini","Amit","rohan","roshan","sneha","neha","bhavya","ramya","arjun","priya",
"Aarav","Vivaan","Aditya","Vihaan","Arjun","Sai","Reyansh","Krishna","Ishaan","Shaurya","Ayaan","Atharv","Dhruv","Kabir","Rudra","Vedant","Aryan",
"Karthik","Yash","Rahul","Nikhil","Manish","Sandeep","Tarun","Deepak","Akash","Ankit","Harsh","Kunal","Pranav","Varun","Siddharth","Abhishek",
"Neeraj","Ravi","Arnav","Om","Priya","Sneha","Ananya","Diya","Kavya","Riya","Pooja","Meera","Isha","Nisha","Aditi","Shruti","Simran","Ritika",
"Tanvi","Swati","Khushi","Muskan","Payal","Divya","Komal","Preeti","Sakshi","Anjali","Sonali","Nandini","Ishita","Madhuri","Shreya","Harini",
"Lakshmi","Keerthi","Bhavya","Sravya","Tejaswi","Navya","Pavani","Manasa","Sowmya","Anusha","Deepika","Keerthana","Amrutha","Chandana","Hema",
"Jyothi","Padma","Rashmi","Sarika","Varsha","Yamini","Zoya","Farah","Ayesha","Sana","Alisha","Noor","Rida","Maira"]

data = pd.DataFrame({

"customer_id": np.arange(1000,1000+rows),
"customer_name": np.random.choice(names,rows),

"app_opened": np.random.randint(0,60,rows),
"session_duration": np.random.randint(1,120,rows),
"avg_time_per_day": np.random.randint(1,180,rows),
"weekly_active_days": np.random.randint(0,7,rows),

"notifications_received": np.random.randint(0,50,rows),
"notifications_clicked": np.random.randint(0,30,rows),
"features_used": np.random.randint(1,15,rows),
"search_count": np.random.randint(0,40,rows),

"referrals_made": np.random.randint(0,10,rows),

"complaints_raised": np.random.randint(0,6,rows),
"support_chat_used": np.random.randint(0,2,rows),
"tickets_resolved": np.random.randint(0,5,rows),

"days_inactive": np.random.randint(0,90,rows),
"last_login_gap": np.random.randint(0,45,rows),

"last_subscription_days": np.random.randint(30,365,rows),
"subscription_renewal_gap": np.random.randint(0,180,rows),

"plan_upgrade_count": np.random.randint(0,5,rows),
"plan_downgrade_count": np.random.randint(0,4,rows),

"auto_renew_enabled": np.random.randint(0,2,rows),

"payment_success": np.random.randint(1,10,rows),
"payment_failures": np.random.randint(0,3,rows),
"refund_requests": np.random.randint(0,5,rows),

"feedback_given": np.random.randint(0,8,rows),
"rating_given": np.random.randint(1,6,rows),

"subscription_price": np.random.choice([199,299,399,499,699,999], rows)

})

# --------------------
# revenue features
# --------------------

data["monthly_spend"] = (
data["subscription_price"]
+ data["plan_upgrade_count"]*120
+ data["features_used"]*8
)

months_active = data["last_subscription_days"] / 30

data["lifetime_value"] = months_active * data["monthly_spend"]

# --------------------
# scores
# --------------------

app_opened_score = 1 - (data["app_opened"] / 60)

duration_score = 1 - (data["session_duration"] / 120)

avg_time_score = 1 - (data["avg_time_per_day"] / 180)

low_activity_score = 1 - (data["weekly_active_days"] / 7)

low_feature_usage_score = 1 - (data["features_used"] / 15)

low_rating_score = 1 - (data["rating_given"] / 6)

complaint_score = data["complaints_raised"] / 6

payment_issue_score = data["payment_failures"] / 3

refund_score = data["refund_requests"] / 5

low_feedback_score = 1 - (data["feedback_given"] / 8)

subscription_recency_score = data["last_subscription_days"] / 365

downgrade_score = data["plan_downgrade_count"] / 4

no_auto_renew_score = 1 - data["auto_renew_enabled"]

renewal_gap_score = data["subscription_renewal_gap"] / 180

monthly_spend_score = data["monthly_spend"] / data["monthly_spend"].max()

lifetime_value_score = data["lifetime_value"] / data["lifetime_value"].max()



churn_probability = (

0.16 * app_opened_score +
0.09 * duration_score +
0.07 * avg_time_score +
0.12 * low_activity_score +
0.07 * low_feature_usage_score +

0.08 * low_rating_score +
0.07 * low_feedback_score +

0.11 * complaint_score +
0.07 * payment_issue_score +
0.06 * refund_score +

0.09 * subscription_recency_score +
0.08 * renewal_gap_score +
0.04 * downgrade_score +
0.03 * no_auto_renew_score +

0.04 * (1 - monthly_spend_score) +
0.02 * (1 - lifetime_value_score)

)

noise = np.random.uniform(0,0.015,rows)

total_prob = churn_probability + noise
total_prob = np.clip(total_prob,0,1)

data["churn"] = (total_prob > 0.60).astype(int)

flip_mask = np.random.rand(rows) < 0.12

data.loc[flip_mask,"churn"] = 1 - data.loc[flip_mask,"churn"]

data.to_csv("customer_dataset.csv",index=False)

print(data["churn"].value_counts())

print("done")