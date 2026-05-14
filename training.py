from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

from sklearn.calibration import CalibratedClassifierCV

import pandas as pd
import numpy as np
import joblib

# =========================================================
# LOAD DATASET
# =========================================================

data = pd.read_csv(
    "customer_dataset.csv"
)

# =========================================================
# REMOVE UNNECESSARY COLUMNS
# =========================================================

x = data.drop(
    columns=[
        "customer_id",
        "customer_name",
        "churn"
    ],
    errors="ignore"
)

# =========================================================
# TARGET
# =========================================================

y = data["churn"]

# =========================================================
# ENCODE PERSONA
# =========================================================

le = LabelEncoder()

x["persona"] = le.fit_transform(
    x["persona"]
)

# =========================================================
# TRAIN TEST SPLIT
# =========================================================

train_x, test_x, train_y, test_y = train_test_split(

    x,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

# =========================================================
# STANDARD SCALING
# ONLY FOR LOGISTIC REGRESSION
# =========================================================

scaler = StandardScaler()

train_x_scaled = scaler.fit_transform(
    train_x
)

test_x_scaled = scaler.transform(
    test_x
)

# =========================================================
# LOGISTIC REGRESSION
# =========================================================

print("\n===================================")
print("LOGISTIC REGRESSION")
print("===================================")

lr_model = LogisticRegression(
    max_iter=5000
)

# training

lr_model.fit(
    train_x_scaled,
    train_y
)

# predictions

lr_pred = lr_model.predict(
    test_x_scaled
)

lr_prob = lr_model.predict_proba(
    test_x_scaled
)[:,1]

# =========================================================
# LOGISTIC REGRESSION METRICS
# =========================================================

print("\nAccuracy:")

print(
    accuracy_score(
        test_y,
        lr_pred
    )
)

print("\nPrecision:")

print(
    precision_score(
        test_y,
        lr_pred
    )
)

print("\nRecall:")

print(
    recall_score(
        test_y,
        lr_pred
    )
)

print("\nF1 Score:")

print(
    f1_score(
        test_y,
        lr_pred
    )
)

print("\nROC AUC Score:")

print(
    roc_auc_score(
        test_y,
        lr_prob
    )
)

print("\nClassification Report:\n")

print(
    classification_report(
        test_y,
        lr_pred
    )
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        test_y,
        lr_pred
    )
)

# =========================================================
# RANDOM FOREST
# =========================================================

print("\n===================================")
print("RANDOM FOREST")
print("===================================")

base_rf = RandomForestClassifier(

    n_estimators=150,

    max_depth=6,

    min_samples_split=10,

    min_samples_leaf=5,

    max_features="sqrt",

    bootstrap=True,

    random_state=42
)

# =========================================================
# PROBABILITY CALIBRATION
# FIXES SUS 1.0 PROBABILITIES
# =========================================================

rf_model = CalibratedClassifierCV(
    base_rf,
    method="sigmoid",
    cv=5
)

# =========================================================
# TRAINING
# =========================================================

rf_model.fit(
    train_x,
    train_y
)

# =========================================================
# PREDICTIONS
# =========================================================

rf_pred = rf_model.predict(
    test_x
)

rf_prob = rf_model.predict_proba(
    test_x
)[:,1]

# =========================================================
# CLIP PROBABILITIES
# AVOID EXACT 0 OR 1
# =========================================================

rf_prob = np.clip(
    rf_prob,
    0.01,
    0.99
)

# =========================================================
# RANDOM FOREST METRICS
# =========================================================

print("\nAccuracy:")

print(
    accuracy_score(
        test_y,
        rf_pred
    )
)

print("\nPrecision:")

print(
    precision_score(
        test_y,
        rf_pred
    )
)

print("\nRecall:")

print(
    recall_score(
        test_y,
        rf_pred
    )
)

print("\nF1 Score:")

print(
    f1_score(
        test_y,
        rf_pred
    )
)

print("\nROC AUC Score:")

print(
    roc_auc_score(
        test_y,
        rf_prob
    )
)

print("\nClassification Report:\n")

print(
    classification_report(
        test_y,
        rf_pred
    )
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        test_y,
        rf_pred
    )
)

# =========================================================
# FEATURE IMPORTANCE
# =========================================================

importance = pd.DataFrame({

    "feature": train_x.columns,

    "importance":

    rf_model.calibrated_classifiers_[0]
    .estimator
    .feature_importances_

})

importance = importance.sort_values(

    by="importance",

    ascending=False

)

print("\n===================================")
print("TOP CHURN FACTORS")
print("===================================\n")

print(
    importance.head(15)
)

# =========================================================
# SAVE MODEL FILES
# =========================================================

joblib.dump(
    rf_model,
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

print("\n===================================")
print("MODEL SAVED SUCCESSFULLY")
print("===================================")

# =========================================================
# SAMPLE PREDICTION PREVIEW
# =========================================================

preview = test_x.copy()

preview["actual_churn"] = test_y.values

preview["predicted_churn"] = rf_pred

preview["churn_probability"] = (
    rf_prob.round(2)
)

print("\n===================================")
print("SAMPLE PREDICTIONS")
print("===================================\n")

print(
    preview[
        [
            "actual_churn",
            "predicted_churn",
            "churn_probability"
        ]
    ].head(20)
)