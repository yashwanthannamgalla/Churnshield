import pandas as pd
import joblib


# ----------------------------
# LOAD DATA
# ----------------------------

def load_data():

    data = pd.read_csv(
        "customer_dataset.csv"
    )

    return data


# ----------------------------
# LOAD MODEL
# ----------------------------

def load_model():

    # change path if model is not inside folder
    model = joblib.load(
        "churn_model.pkl"
    )

    return model


# ----------------------------
# PREDICT CHURN
# ----------------------------

def predict_churn(model,data):

    X = data.drop(
        ["customer_id","customer_name","churn"],
        axis=1
    )

    probs = model.predict_proba(X)

    data["churn_probability"] = probs[:,1]

    return data,X


# ----------------------------
# GLOBAL FEATURE IMPORTANCE
# ----------------------------

def get_feature_importance(model,X):

    importance = model.coef_[0]

    scores = pd.Series(
        importance,
        index=X.columns
    )

    top_feature = scores.abs().idxmax()

    return scores,top_feature


# ----------------------------
# CUSTOMER SPECIFIC REASON
# ----------------------------

def get_customer_reason(model,X):

    coefs = model.coef_[0]

    impact = X.mul(coefs)

    reasons = impact.abs().idxmax(
        axis=1
    )

    return reasons
# ----------------------------
# BUSINESS METRICS
# ----------------------------

def calculate_business_metrics(data):

    base_price = 199   # monthly subscription

    engagement_factor = (

        data["weekly_active_days"]/7 +

        data["avg_time_per_day"]/120 +

        data["features_used"]/10

    )

    loyalty_factor = 1 + (

        data["plan_upgrade_count"]*0.2 -

        data["plan_downgrade_count"]*0.1

    )


    # monthly revenue
    data["monthly_revenue"] = (

        base_price *

        (1 + engagement_factor) *

        loyalty_factor

    ).clip(99,999)


    # yearly revenue
    data["yearly_revenue"] = (

        data["monthly_revenue"] * 12

    )


    # retention spending estimate
    data["retention_cost"] = (

        50 +   # base offer cost

        20*data["complaints_raised"] +

        10*data["refund_requests"]

    ).clip(50,300)


    return data