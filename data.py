import pandas as pd
import numpy as np

np.random.seed(42)

rows = 5000

# =========================================================
# CUSTOMER NAMES
# =========================================================

names = [
    "Yashwanth","Vikram","Shiva","Amit","Rohan","Sneha",
    "Priya","Ananya","Rahul","Arjun","Pooja","Khushi",
    "Sana","Om","Abhishek","Shruti","Tejaswi","Manasa",
    "Bhavya","Ritika","Nandini","Harini","Keerthi"
]

# =========================================================
# PERSONAS
# =========================================================

personas = {
    "loyal_power_user": 0.20,
    "regular_user": 0.35,
    "premium_customer": 0.10,
    "casual_user": 0.15,
    "at_risk_user": 0.12,
    "angry_customer": 0.08
}

persona_choices = list(personas.keys())
persona_probs = list(personas.values())

persona_list = np.random.choice(
    persona_choices,
    rows,
    p=persona_probs
)

# =========================================================
# DATA STORAGE
# =========================================================

data = []

# =========================================================
# CUSTOMER GENERATION
# =========================================================

for i in range(rows):

    p = persona_list[i]

    customer = {}

    # =====================================================
    # BASIC INFO
    # =====================================================

    customer["customer_id"] = 1000 + i
    customer["customer_name"] = np.random.choice(names)
    customer["persona"] = p

    # =====================================================
    # PERSONA STATES
    # =====================================================

    if p == "loyal_power_user":

        engagement = np.random.randint(65, 98)

        weekly_active_days = np.random.randint(4, 8)

        app_opened = np.random.randint(30, 60)

        features_used = np.random.randint(8, 15)

        complaints_raised = np.random.randint(0, 3)

        rating_given = np.random.randint(3, 6)

        refund_requests = np.random.randint(0, 2)

        feedback_given = np.random.randint(3, 8)

        days_inactive = np.random.randint(0, 15)

        last_login_gap = np.random.randint(0, 5)

        subscription_price = np.random.choice([499,699,999])

        auto_renew_enabled = np.random.choice([0,1], p=[0.1,0.9])

        plan_upgrade_count = np.random.randint(1, 5)

        plan_downgrade_count = np.random.randint(0, 2)

        last_subscription_days = np.random.randint(180, 366)

        subscription_renewal_gap = np.random.randint(0, 20)

        referrals_made = np.random.randint(1, 8)

        search_count = np.random.randint(10, 45)

    elif p == "regular_user":

        engagement = np.random.randint(45, 85)

        weekly_active_days = np.random.randint(2, 7)

        app_opened = weekly_active_days * np.random.randint(4, 9)

        features_used = np.random.randint(4, 12)

        complaints_raised = np.random.randint(0, 4)

        rating_given = np.random.randint(2, 6)

        refund_requests = np.random.randint(0, 3)

        feedback_given = np.random.randint(1, 6)

        days_inactive = np.random.randint(5, 35)

        last_login_gap = np.random.randint(1, 15)

        subscription_price = np.random.choice([299,399,499])

        auto_renew_enabled = np.random.choice([0,1], p=[0.4,0.6])

        plan_upgrade_count = np.random.randint(0, 3)

        plan_downgrade_count = np.random.randint(0, 3)

        last_subscription_days = np.random.randint(100, 320)

        subscription_renewal_gap = np.random.randint(5, 60)

        referrals_made = np.random.randint(0, 4)

        search_count = np.random.randint(5, 30)

    elif p == "premium_customer":

        engagement = np.random.randint(60, 95)

        weekly_active_days = np.random.randint(3, 7)

        app_opened = np.random.randint(25, 55)

        features_used = np.random.randint(7, 15)

        complaints_raised = np.random.randint(0, 3)

        rating_given = np.random.randint(3, 6)

        refund_requests = np.random.randint(0, 2)

        feedback_given = np.random.randint(2, 7)

        days_inactive = np.random.randint(0, 20)

        last_login_gap = np.random.randint(0, 8)

        subscription_price = np.random.choice([699,999])

        auto_renew_enabled = np.random.choice([0,1], p=[0.15,0.85])

        plan_upgrade_count = np.random.randint(1, 5)

        plan_downgrade_count = np.random.randint(0, 2)

        last_subscription_days = np.random.randint(180, 365)

        subscription_renewal_gap = np.random.randint(0, 30)

        referrals_made = np.random.randint(1, 6)

        search_count = np.random.randint(10, 40)

    elif p == "casual_user":

        engagement = np.random.randint(30, 70)

        weekly_active_days = np.random.randint(1, 5)

        app_opened = weekly_active_days * np.random.randint(3, 8)

        features_used = np.random.randint(2, 9)

        complaints_raised = np.random.randint(0, 4)

        rating_given = np.random.randint(1, 5)

        refund_requests = np.random.randint(0, 3)

        feedback_given = np.random.randint(0, 5)

        days_inactive = np.random.randint(10, 50)

        last_login_gap = np.random.randint(3, 25)

        subscription_price = np.random.choice([199,299,399])

        auto_renew_enabled = np.random.choice([0,1], p=[0.6,0.4])

        plan_upgrade_count = np.random.randint(0, 2)

        plan_downgrade_count = np.random.randint(0, 3)

        last_subscription_days = np.random.randint(50, 220)

        subscription_renewal_gap = np.random.randint(15, 90)

        referrals_made = np.random.randint(0, 2)

        search_count = np.random.randint(2, 18)

    elif p == "at_risk_user":

        engagement = np.random.randint(20, 65)

        weekly_active_days = np.random.randint(0, 4)

        app_opened = weekly_active_days * np.random.randint(1, 6)

        features_used = np.random.randint(1, 7)

        complaints_raised = np.random.randint(1, 6)

        rating_given = np.random.randint(1, 4)

        refund_requests = np.random.randint(1, 4)

        feedback_given = np.random.randint(0, 3)

        days_inactive = np.random.randint(20, 90)

        last_login_gap = np.random.randint(10, 50)

        subscription_price = np.random.choice([199,299,399])

        auto_renew_enabled = np.random.choice([0,1], p=[0.85,0.15])

        plan_upgrade_count = np.random.randint(0, 1)

        plan_downgrade_count = np.random.randint(1, 4)

        last_subscription_days = np.random.randint(20, 150)

        subscription_renewal_gap = np.random.randint(40, 180)

        referrals_made = np.random.randint(0, 1)

        search_count = np.random.randint(0, 10)

    else:

        engagement = np.random.randint(25, 70)

        weekly_active_days = np.random.randint(1, 5)

        app_opened = weekly_active_days * np.random.randint(2, 7)

        features_used = np.random.randint(2, 8)

        complaints_raised = np.random.randint(2, 7)

        rating_given = np.random.randint(1, 4)

        refund_requests = np.random.randint(1, 5)

        feedback_given = np.random.randint(0, 3)

        days_inactive = np.random.randint(15, 70)

        last_login_gap = np.random.randint(8, 35)

        subscription_price = np.random.choice([199,299,399,499])

        auto_renew_enabled = np.random.choice([0,1], p=[0.9,0.1])

        plan_upgrade_count = np.random.randint(0, 1)

        plan_downgrade_count = np.random.randint(1, 3)

        last_subscription_days = np.random.randint(30, 180)

        subscription_renewal_gap = np.random.randint(40, 150)

        referrals_made = np.random.randint(0, 1)

        search_count = np.random.randint(1, 15)

    # =====================================================
    # RECOVERY BEHAVIOR
    # =====================================================

    re_engaged_user = np.random.choice(
        [0,1],
        p=[0.80,0.20]
    )

    if re_engaged_user == 1:

        engagement += np.random.randint(5,20)

        engagement = np.clip(
            engagement,
            1,
            100
        )

        complaints_raised = max(
            0,
            complaints_raised - np.random.randint(0,2)
        )

        rating_given = min(
            5,
            rating_given + np.random.randint(0,2)
        )

        refund_requests = max(
            0,
            refund_requests - np.random.randint(0,2)
        )

        weekly_active_days = min(
            7,
            weekly_active_days + np.random.randint(0,2)
        )

        app_opened += np.random.randint(3,10)

    # =====================================================
    # SESSION DEPENDENCY
    # =====================================================

    base_session = (
        app_opened
        * np.random.uniform(1.8,3.5)
    )

    session_duration = int(
        np.clip(
            base_session,
            5,
            180
        )
    )

    # =====================================================
    # AVG TIME PER DAY
    # =====================================================

    avg_time_per_day = int(
        np.clip(
            (
                session_duration
                / max(1, weekly_active_days)
            )
            + np.random.randint(5,20),
            5,
            240
        )
    )

    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    notifications_received = int(
        np.clip(
            (
                app_opened // 2
                + weekly_active_days * 2
                + features_used
                + np.random.randint(2,12)
            ),
            5,
            50
        )
    )

    click_rate = np.clip(
        (
            engagement / 100
            + np.random.normal(0,0.10)
        ),
        0.05,
        0.95
    )

    notifications_clicked = int(
        notifications_received
        * click_rate
    )

    # =====================================================
    # SUPPORT SYSTEM
    # =====================================================

    support_quality = np.random.choice(
        ["excellent","average","poor"],
        p=[0.25,0.50,0.25]
    )

    if support_quality == "excellent":

        tickets_resolved = max(
            0,
            complaints_raised - np.random.randint(0,1)
        )

    elif support_quality == "average":

        tickets_resolved = max(
            0,
            complaints_raised - np.random.randint(0,3)
        )

    else:

        tickets_resolved = np.random.randint(
            0,
            max(1, complaints_raised)
        )

    support_chat_used = int(
        complaints_raised >= 2
    )

    # =====================================================
    # ACCOUNT AGE + REVENUE
    # =====================================================

    account_age_months = np.random.randint(
        max(2, last_subscription_days // 30),
        60
    )

    monthly_spend = (
        subscription_price
        + plan_upgrade_count * 120
        + features_used * 10
    )

    lifetime_value = int(
        monthly_spend
        * account_age_months
    )

    # =====================================================
    # PAYMENT DEPENDENCY
    # =====================================================

    payment_success = int(
        np.clip(
            (
                account_age_months // 8
                + engagement // 25
                + auto_renew_enabled * 2
                - complaints_raised
                + np.random.randint(-2,3)
            ),
            1,
            10
        )
    )

    payment_failures = int(
        np.clip(
            (
                4
                - payment_success // 3
                + complaints_raised // 2
                + np.random.randint(0,3)
            ),
            0,
            4
        )
    )

        # =====================================================
    # CHURN SCORE
    # =====================================================

    churn_score = 0

    # =====================================================
    # BAD SIGNALS
    # =====================================================

    if engagement < 40:
        churn_score += 3

    if complaints_raised >= 3:
        churn_score += 2

    if payment_failures >= 2:
        churn_score += 2

    if refund_requests >= 2:
        churn_score += 2

    if days_inactive > 40:
        churn_score += 3

    if auto_renew_enabled == 0:
        churn_score += 2

    if rating_given <= 2:
        churn_score += 2

    if weekly_active_days <= 2:
        churn_score += 2

    if notifications_clicked < (
        notifications_received * 0.25
    ):
        churn_score += 1

    if plan_downgrade_count >= 1:
        churn_score += 1

    # =====================================================
    # EXTRA BAD SIGNALS
    # =====================================================

    if app_opened < 10:
        churn_score += 2

    if features_used <= 3:
        churn_score += 2

    if search_count < 5:
        churn_score += 1

    if session_duration < 20:
        churn_score += 2

    if avg_time_per_day < 15:
        churn_score += 1

    if lifetime_value < 5000:
        churn_score += 2

    # =====================================================
    # GOOD SIGNALS
    # =====================================================

    if engagement > 75:
        churn_score -= 3

    if weekly_active_days >= 5:
        churn_score -= 2

    if rating_given >= 4:
        churn_score -= 2

    if referrals_made >= 2:
        churn_score -= 1

    if auto_renew_enabled == 1:
        churn_score -= 2

    if complaints_raised == 0:
        churn_score -= 1

    # =====================================================
    # EXTRA GOOD SIGNALS
    # =====================================================

    if app_opened > 35:
        churn_score -= 2

    if features_used >= 8:
        churn_score -= 2

    if session_duration > 60:
        churn_score -= 2

    if avg_time_per_day > 45:
        churn_score -= 1

    if lifetime_value > 20000:
        churn_score -= 2

    if search_count > 20:
        churn_score -= 1

    if feedback_given >= 4:
        churn_score -= 1

    # =====================================================
    # CONTROLLED RANDOMNESS
    # =====================================================

    churn_score += np.random.randint(-1, 2)

    # =====================================================
    # CONVERT TO PROBABILITY
    # =====================================================

    churn_probability = 1 / (
        1 + np.exp(-0.38 * churn_score)
    )

    # =====================================================
    # FINAL LABEL
    # =====================================================

    churn = np.random.binomial(
        1,
        churn_probability
    )

    # =====================================================
    # CONTROLLED RANDOMNESS
    # =====================================================

    churn_probability += np.random.normal(
        0,
        0.04
    )

    random_behavior = np.random.uniform(
        -0.03,
        0.05
    )

    churn_probability += random_behavior

    churn_probability = np.clip(
        churn_probability,
        0,
        1
    )

    # =====================================================
    # FINAL CHURN LABEL
    # =====================================================

    churn = np.random.binomial(
        1,
        churn_probability
    )

    # =====================================================
    # SAVE FEATURES
    # =====================================================

    customer["engagement_score"] = engagement

    customer["app_opened"] = app_opened
    customer["session_duration"] = session_duration
    customer["avg_time_per_day"] = avg_time_per_day
    customer["weekly_active_days"] = weekly_active_days

    customer["notifications_received"] = notifications_received
    customer["notifications_clicked"] = notifications_clicked

    customer["features_used"] = features_used
    customer["search_count"] = search_count

    customer["referrals_made"] = referrals_made

    customer["complaints_raised"] = complaints_raised
    customer["support_chat_used"] = support_chat_used
    customer["tickets_resolved"] = tickets_resolved

    customer["days_inactive"] = days_inactive
    customer["last_login_gap"] = last_login_gap

    customer["last_subscription_days"] = last_subscription_days
    customer["subscription_renewal_gap"] = subscription_renewal_gap

    customer["plan_upgrade_count"] = plan_upgrade_count
    customer["plan_downgrade_count"] = plan_downgrade_count

    customer["auto_renew_enabled"] = auto_renew_enabled

    customer["payment_success"] = payment_success
    customer["payment_failures"] = payment_failures
    customer["refund_requests"] = refund_requests

    customer["feedback_given"] = feedback_given
    customer["rating_given"] = rating_given

    customer["subscription_price"] = subscription_price

    customer["monthly_spend"] = monthly_spend

    customer["account_age_months"] = account_age_months

    customer["lifetime_value"] = lifetime_value

    customer["churn"] = churn

    data.append(customer)

# =========================================================
# FINAL DATAFRAME
# =========================================================

df = pd.DataFrame(data)

# =========================================================
# SAVE CSV
# =========================================================

df.to_csv(
    "customer_dataset.csv",
    index=False
)

print(df.head())

print("\nChurn Distribution:\n")
print(df["churn"].value_counts())

print("\nDataset Generated Successfully")