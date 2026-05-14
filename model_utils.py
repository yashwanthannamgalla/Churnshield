# =====================================================
# MODEL_UTILS.PY
# =====================================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    data = pd.read_csv(
        "customer_dataset.csv"
    )

    return data


# =====================================================
# LOAD MODEL
# =====================================================

def load_model():

    model = joblib.load(
        "churn_model.pkl"
    )

    return model


# =====================================================
# PREDICT CHURN
# =====================================================

def predict_churn(model, data):

    df = data.copy()

    X = df.drop(
        columns=[
            "customer_id",
            "customer_name",
            "churn"
        ],
        errors="ignore"
    )

    # encode categorical feature
    le = joblib.load(
        "label_encoder.pkl"
    )

    X["persona"] = le.transform(
        X["persona"]
    )

    # predictions
    predictions = model.predict(X)

    probabilities = model.predict_proba(X)[:, 1]

    # save results
    df["predicted_churn"] = predictions

    df["churn_probability"] = (
        probabilities
    ).round(4)

    return df, X


# =====================================================
# FEATURE IMPORTANCE
# =====================================================
def get_feature_importance(model, X):

    # calibrated model
    if hasattr(model, "calibrated_classifiers_"):

        rf_model = (
            model.calibrated_classifiers_[0]
            .estimator
        )

    # normal random forest
    else:

        rf_model = model

    feature_scores = pd.Series(

        rf_model.feature_importances_,

        index=X.columns

    )

    feature_scores = feature_scores.sort_values(
        ascending=False
    )

    top_feature = feature_scores.index[0]

    return feature_scores, top_feature


# =====================================================
# CUSTOMER CHURN REASONS
# =====================================================

def get_customer_reason(data):

    reasons = []

    for _, row in data.iterrows():

        customer_reasons = []

        if row["engagement_score"] < 40:
            customer_reasons.append(
                "Low Engagement"
            )

        if row["days_inactive"] > 40:
            customer_reasons.append(
                "Inactive User"
            )

        if row["complaints_raised"] >= 3:
            customer_reasons.append(
                "Too Many Complaints"
            )

        if row["payment_failures"] >= 2:
            customer_reasons.append(
                "Payment Failures"
            )

        if row["refund_requests"] >= 2:
            customer_reasons.append(
                "Frequent Refund Requests"
            )

        if row["weekly_active_days"] <= 2:
            customer_reasons.append(
                "Low Weekly Activity"
            )

        if row["auto_renew_enabled"] == 0:
            customer_reasons.append(
                "Auto Renew Disabled"
            )

        if row["rating_given"] <= 2:
            customer_reasons.append(
                "Low Rating Given"
            )

        if row["features_used"] <= 3:
            customer_reasons.append(
                "Low Feature Usage"
            )

        if row["session_duration"] < 20:
            customer_reasons.append(
                "Low Session Duration"
            )

        # fallback
        if len(customer_reasons) == 0:

            customer_reasons.append(
                "Healthy Customer"
            )

        reasons.append(
            ", ".join(customer_reasons)
        )

    return reasons


# =====================================================
# BUSINESS METRICS
# =====================================================

def calculate_business_metrics(data):

    df = data.copy()

    # yearly revenue
    df["yearly_revenue"] = (
        df["monthly_spend"] * 12
    )

    # retention spending estimate
    retention_costs = []

    for _, row in df.iterrows():

        if row["churn_probability"] > 0.8:

            retention_costs.append(3000)

        elif row["churn_probability"] > 0.5:

            retention_costs.append(1500)

        else:

            retention_costs.append(500)

    df["retention_cost"] = retention_costs

    return df


# =====================================================
# TRAIN MODEL
# =====================================================

def train_model():

    data = load_data()

    # remove non-feature columns
    train_df = data.drop(
        columns=[
            "customer_id",
            "customer_name"
        ],
        errors="ignore"
    )

    # encode persona
    le = LabelEncoder()

    train_df["persona"] = le.fit_transform(
        train_df["persona"]
    )

    # features and target
    X = train_df.drop(
        "churn",
        axis=1
    )

    y = train_df["churn"]

    # split
    x_train, x_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # scaling for logistic regression
    scaler = StandardScaler()

    x_train_scaled = scaler.fit_transform(
        x_train
    )

    x_test_scaled = scaler.transform(
        x_test
    )

    # logistic regression
    lr_model = LogisticRegression(
        max_iter=2000
    )

    lr_model.fit(
        x_train_scaled,
        y_train
    )

    lr_preds = lr_model.predict(
        x_test_scaled
    )

    lr_acc = accuracy_score(
        y_test,
        lr_preds
    )

    # random forest
    rf_model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        random_state=42
    )

    rf_model.fit(
        x_train,
        y_train
    )

    rf_preds = rf_model.predict(
        x_test
    )

    rf_acc = accuracy_score(
        y_test,
        rf_preds
    )

    # use random forest
    best_model = rf_model

    # save files
    joblib.dump(
        best_model,
        "churn_model.pkl"
    )

    joblib.dump(
        scaler,
        "scaler.pkl"
    )

    joblib.dump(
        le,
        "label_encoder.pkl"
    )

    # logs
    print("\n======================")
    print("MODEL RESULTS")
    print("======================")

    print(
        f"\nLogistic Regression Accuracy: {round(lr_acc,3)}"
    )

    print(
        f"Random Forest Accuracy: {round(rf_acc,3)}"
    )

    print("\n======================")
    print("CLASSIFICATION REPORT")
    print("======================")

    print(
        classification_report(
            y_test,
            rf_preds
        )
    )

    print("\nModel training completed ✅")


# =====================================================
# RUN TRAINING
# =====================================================

if __name__ == "__main__":

    train_model()