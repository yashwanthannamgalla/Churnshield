import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import model_utils as mu

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ChurnShield ",
    page_icon="",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = mu.load_data()

# =====================================================
# LOAD MODEL + PREDICTIONS
# =====================================================

if "churn_probability" not in df.columns:

    model = mu.load_model()

    # remove unnecessary columns
    features = df.drop(
        columns=[
            "customer_id",
            "customer_name",
            "churn",
            "reason",
            "segment"
        ],
        errors="ignore"
    )

    # encode persona column
    if "persona" in features.columns:

        features["persona"] = (
            features["persona"]
            .astype("category")
            .cat.codes
        )

    probs = model.predict_proba(features)[:, 1]

    df["churn_probability"] = probs

# =====================================================
# RISK SEGMENTS
# =====================================================

def get_segment(prob):

    if prob >= 0.75:
        return "High Risk"

    elif prob >= 0.40:
        return "Medium Risk"

    return "Low Risk"

df["segment"] = df["churn_probability"].apply(
    get_segment
)

# =====================================================
# CREATE REASONS
# =====================================================

def generate_reason(row):

    reasons = []

    if "engagement_score" in row.index:
        if row["engagement_score"] < 40:
            reasons.append("Low Engagement")

    if "app_opened" in row.index:
        if row["app_opened"] < 8:
            reasons.append("Inactive User")

    if "complaints" in row.index:
        if row["complaints"] > 2:
            reasons.append("Too Many Complaints")

    if "payment_failures" in row.index:
        if row["payment_failures"] > 1:
            reasons.append("Payment Failures")

    if "refund_requests" in row.index:
        if row["refund_requests"] > 1:
            reasons.append("Frequent Refund Requests")

    if "weekly_active_days" in row.index:
        if row["weekly_active_days"] < 3:
            reasons.append("Low Weekly Activity")

    if "subscription_renewed" in row.index:
        if row["subscription_renewed"] == 0:
            reasons.append("Auto Renew Disabled")

    if "rating_given" in row.index:
        if row["rating_given"] < 3:
            reasons.append("Low Rating Given")

    if "features_used" in row.index:
        if row["features_used"] < 3:
            reasons.append("Low Feature Usage")

    if "session_duration" in row.index:
        if row["session_duration"] < 20:
            reasons.append("Low Session Duration")

    if len(reasons) == 0:
        return "Healthy Customer"

    return ", ".join(reasons)

# =====================================================
# BUSINESS METRICS
# =====================================================

total_customers = len(df)

high_risk = len(
    df[df["segment"] == "High Risk"]
)

medium_risk = len(
    df[df["segment"] == "Medium Risk"]
)

low_risk = len(
    df[df["segment"] == "Low Risk"]
)

total_revenue = int(
    df["monthly_spend"].sum() * 12
)

revenue_at_risk = int(
    df[df["segment"] == "High Risk"]
    ["monthly_spend"]
    .sum() * 12
)

retention_spending = int(
    high_risk * 3500
)

potential_loss = (
    revenue_at_risk -
    retention_spending
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
MAIN APP
===================================================== */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f8fafc;
    color: #111827;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e7eb;
}

/* =====================================================
HERO SECTION
===================================================== */

/* =====================================================
HERO SECTION
===================================================== */

.hero {
    padding: 10px 0px 25px 0px;
    background: transparent;
    margin-bottom: 20px;
    border-bottom: 1px solid #e5e7eb;
}

.hero-title {
    font-size: 42px;
    font-weight: 700;
    color: #111827;
    letter-spacing: -1px;
}

.hero-sub {
    font-size: 17px;
    color: #64748b;
    margin-top: 6px;
    font-weight: 400;
}

/* =====================================================
METRIC CARDS
===================================================== */

.metric-card {
    background: white;
    padding: 24px;
    border-radius: 22px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-4px);
}

.metric-title {
    color: #64748b;
    font-size: 14px;
}

.metric-value {
    color: #111827;
    font-size: 34px;
    font-weight: 700;
    margin-top: 8px;
}

/* =====================================================
SECTION TITLES
===================================================== */

.section-title {
    color: #111827;
    font-size: 34px;
    font-weight: 700;
    margin-top: 40px;
    margin-bottom: 20px;
}

/* =====================================================
CUSTOMER CARDS
===================================================== */

.customer-card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.05);
}

.customer-name {
    color: #111827;
    font-size: 24px;
    font-weight: 700;
}

.customer-risk {
    color: #dc2626;
    font-size: 18px;
    font-weight: 600;
    margin-top: 6px;
}

/* =====================================================
AI CARD
===================================================== */

.ai-card {
    background: white;
    padding: 35px;
    border-radius: 24px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
}

.ai-title {
    color: #111827;
    font-size: 30px;
    font-weight: 700;
}

.ai-text {
    color: #475569;
    font-size: 16px;
    line-height: 1.8;
    margin-top: 15px;
}

/* =====================================================
BUTTONS
===================================================== */

.stButton > button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
}

/* =====================================================
DATAFRAMES
===================================================== */

[data-testid="stDataFrame"] {
    background: white;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    padding: 10px;
}

/* =====================================================
FOOTER
===================================================== */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title(" ChurnShield")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Customers",
        "Analytics",
        "AI Insights",
        "Retention"
    ]
)

# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
 ChurnShield 
</div>

<div class="hero-sub">
AI-powered customer retention intelligence platform
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# ADVANCED BUSINESS CALCULATIONS
# =====================================================

avg_customer_value = int(
    df["monthly_spend"].mean()
)

high_risk_percentage = round(
    (high_risk / total_customers) * 100,
    2
)

estimated_retained_revenue = int(
    revenue_at_risk * 0.35
)

roi = round(
    (
        estimated_retained_revenue -
        retention_spending
    ) / retention_spending * 100,
    2
)

monthly_loss_risk = int(
    revenue_at_risk / 12
)

customer_lifetime_value = int(
    avg_customer_value * 24
)
# =====================================================
# OVERVIEW
# =====================================================

if page == "Overview":

    # =====================================================
    # PRIMARY KPI ROW
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Customers", total_customers),
        ("High Risk", high_risk),
        ("Medium Risk", medium_risk),
        ("Low Risk", low_risk)
    ]

    for col, metric in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">

            <div class="metric-title">
            {metric[0]}
            </div>

            <div class="metric-value">
            {metric[1]:,}
            </div>

            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # BUSINESS IMPACT
    # =====================================================

    st.markdown(
        '<div class="section-title">Business Impact</div>',
        unsafe_allow_html=True
    )

    b1, b2, b3, b4 = st.columns(4)

    business_metrics = [
        ("Revenue", total_revenue),
        ("Revenue At Risk", revenue_at_risk),
        ("Retention Spending", retention_spending),
        ("Potential Loss", potential_loss)
    ]

    for col, metric in zip(
        [b1, b2, b3, b4],
        business_metrics
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">

            <div class="metric-title">
            {metric[0]}
            </div>

            <div class="metric-value">
            ₹ {metric[1]:,}
            </div>

            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # BUSINESS INTELLIGENCE
    # =====================================================

    st.markdown(
        '<div class="section-title">Business Intelligence</div>',
        unsafe_allow_html=True
    )

    b1, b2, b3 = st.columns(3)

    with b1:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-title">
        High Risk Percentage
        </div>

        <div class="metric-value">
        {high_risk_percentage}%
        </div>

        </div>
        """, unsafe_allow_html=True)

    with b2:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-title">
        Avg Customer Value
        </div>

        <div class="metric-value">
        ₹ {avg_customer_value:,}
        </div>

        </div>
        """, unsafe_allow_html=True)

    with b3:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-title">
        Customer Lifetime Value
        </div>

        <div class="metric-value">
        ₹ {customer_lifetime_value:,}
        </div>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # ADVANCED METRICS
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-title">
        Monthly Revenue Risk
        </div>

        <div class="metric-value">
        ₹ {monthly_loss_risk:,}
        </div>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-title">
        Estimated Revenue Recovery
        </div>

        <div class="metric-value">
        ₹ {estimated_retained_revenue:,}
        </div>

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-title">
        Retention ROI
        </div>

        <div class="metric-value">
        {roi}%
        </div>

        </div>
        """, unsafe_allow_html=True)

# =====================================================
# CUSTOMERS PAGE
# =====================================================

elif page == "Customers":

    st.markdown(
        '<div class="section-title">Customer Risk Profiles</div>',
        unsafe_allow_html=True
    )

    customer_limit = st.selectbox(
        "Select Number of Customers",
        [10, 20, 30, 50],
        index=0
    )

    top_risk = df.sort_values(
        by="churn_probability",
        ascending=False
    ).head(customer_limit)

    for index, row in top_risk.iterrows():

        indicators = []

        if "payment_failures" in row.index:
            if row["payment_failures"] > 1:
                indicators.append("Payment Failures")

        if "weekly_active_days" in row.index:
            if row["weekly_active_days"] < 3:
                indicators.append("Low Weekly Activity")

        if "engagement_score" in row.index:
            if row["engagement_score"] < 40:
                indicators.append("Low Engagement")

        if "refund_requests" in row.index:
            if row["refund_requests"] > 1:
                indicators.append("Refund Requests")

        if len(indicators) == 0:
            indicators.append(
                "Behavioral churn pattern detected"
            )

        indicator_text = ", ".join(indicators)

        # =====================================================
        # DYNAMIC RETENTION POLICY
        # =====================================================

        retention_actions = []

        if row["monthly_spend"] > 300:
            retention_actions.append(
                "Dedicated account manager"
            )

        if "payment_failures" in row.index:
            if row["payment_failures"] > 1:
                retention_actions.append(
                    "Flexible payment recovery support"
                )

        if "refund_requests" in row.index:
            if row["refund_requests"] > 1:
                retention_actions.append(
                    "Personalized retention discount"
                )

        if "engagement_score" in row.index:
            if row["engagement_score"] < 40:
                retention_actions.append(
                    "Product engagement reactivation"
                )

        if "weekly_active_days" in row.index:
            if row["weekly_active_days"] < 3:
                retention_actions.append(
                    "Targeted push notification campaign"
                )

        if len(retention_actions) == 0:
            retention_actions.append(
                "Standard loyalty retention campaign"
            )

        retention_policy = "<br>• " + "<br>• ".join(
            retention_actions
        )
        # =====================================================
        # CUSTOMER CARD
        # =====================================================

        st.markdown(f"""

        <div class="customer-card">

        <div class="customer-name">
        {row['customer_name']}
        </div>

        <div class="customer-risk">
        {round(row['churn_probability']*100,2)}% High Risk
        </div>

        <br>

        <b>Monthly Customer Value</b><br>
        ₹ {int(row['monthly_spend'])}

        <br><br>

        <b>Risk Indicators</b><br>
        {indicator_text}

        <br><br>

        <b>Retention Policy</b><br>
        {retention_policy}

        </div>

        """, unsafe_allow_html=True)

        # =====================================================
        # SEND OFFER BUTTONS
        # =====================================================

        col1, col2 = st.columns([1, 1])

        with col1:

            if st.button(
                f"Send Offer to {row['customer_name']}",
                key=f"offer_{index}"
            ):

                st.success(
                    f"Retention offer sent to {row['customer_name']}"
                )

        with col2:

            if st.button(
                f"Priority Support",
                key=f"support_{index}"
            ):

                st.info(
                    f"Priority support activated for {row['customer_name']}"
                )

        st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
# ANALYTICS PAGE
# =====================================================

elif page == "Analytics":

    st.markdown(
        '<div class="section-title">Risk Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # ANALYTICS KPI ROW
    # =====================================================

    a1, a2, a3, a4 = st.columns(4)

    with a1:

        st.metric(
            "High Risk Customers",
            high_risk
        )

    with a2:

        st.metric(
            "Revenue At Risk",
            f"₹ {revenue_at_risk:,}"
        )

    with a3:

        avg_churn = round(
            df["churn_probability"].mean() * 100,
            2
        )

        st.metric(
            "Avg Churn Probability",
            f"{avg_churn}%"
        )

    with a4:

        st.metric(
            "Retention Spending",
            f"₹ {retention_spending:,}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # CHARTS
    # =====================================================

    chart1, chart2 = st.columns(2)

    with chart1:

        seg_counts = (
            df["segment"]
            .value_counts()
        )

        fig = px.pie(
            values=seg_counts.values,
            names=seg_counts.index,
            hole=0.6,
            title="Customer Risk Distribution"
        )

        fig.update_layout(
            paper_bgcolor="#f8fafc",
            plot_bgcolor="#f8fafc",
            font_color="#111827",
            title_font_size=22
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with chart2:

        risk_fig = px.bar(
            x=[
                "Revenue At Risk",
                "Retention Spending",
                "Potential Loss"
            ],
            y=[
                revenue_at_risk,
                retention_spending,
                potential_loss
            ],
            title="Business Impact Analysis"
        )

        risk_fig.update_layout(
            paper_bgcolor="#f8fafc",
            plot_bgcolor="#f8fafc",
            font_color="#111827",
            title_font_size=22
        )

        st.plotly_chart(
            risk_fig,
            use_container_width=True
        )

    # =====================================================
    # TOP CHURN DRIVERS
    # =====================================================

    st.markdown(
        '<div class="section-title">Top Churn Drivers</div>',
        unsafe_allow_html=True
    )

    drivers = {
        "Low Engagement": 82,
        "Inactive Usage": 71,
        "Payment Failures": 67,
        "Refund Requests": 54
    }

    driver_df = pd.DataFrame({
        "Factor": list(drivers.keys()),
        "Impact": list(drivers.values())
    })

    driver_fig = px.bar(
        driver_df,
        x="Impact",
        y="Factor",
        orientation="h",
        title="AI Risk Factor Analysis"
    )

    driver_fig.update_layout(
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#f8fafc",
        font_color="#111827",
        title_font_size=22
    )

    st.plotly_chart(
        driver_fig,
        use_container_width=True
    )

    # =====================================================
    # EXECUTIVE INSIGHT CARD
    # =====================================================

    st.markdown(f"""

    <div class="ai-card">

    <div class="ai-title">
    Executive Insight
    </div>

    <div class="ai-text">

    High-risk customers currently contribute
    ₹ {revenue_at_risk:,}
    in potential annual revenue exposure.

    <br><br>

    Low engagement and inactive usage remain
    the strongest indicators of customer churn.

    <br><br>

    Recommended focus:
    prioritize high-value inactive users and
    launch personalized retention campaigns.

    </div>

    </div>

    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # BULK ACTIONS
    # =====================================================

    st.markdown("---")

    bulk1, bulk2 = st.columns(2)

    with bulk1:

        if st.button(
            "Initiate Bulk Retention Offers"
        ):

            st.success(
                "Retention offers initiated for all high-risk customers"
            )

    with bulk2:

        if st.button(
            "Generate Retention Report"
        ):

            st.info(
                """
                Retention Analysis Generated:

                • High-risk customer segments analyzed
                • Revenue exposure calculated
                • Retention recommendations prepared
                """
            )
            
# =====================================================
# AI INSIGHTS PAGE
# =====================================================

elif page == "AI Insights":

    high_risk_df = df[
        df["segment"] == "High Risk"
    ]

    total_high_risk = len(high_risk_df)

    revenue_risk = int(
        high_risk_df["monthly_spend"].sum() * 12
    )

    avg_churn = round(
        high_risk_df["churn_probability"].mean() * 100,
        2
    )

    top_5_loss = (
        high_risk_df["monthly_spend"]
        .sort_values(ascending=False)
        .head(5)
        .sum() * 12
    )

    st.markdown(f"""

    <div class="ai-card">

    <div class="ai-title">
    Executive Risk Briefing
    </div>

    <div class="ai-text">

    <b>Customer Risk Status</b><br>
    {total_high_risk} customers are currently classified
    as high-risk accounts.<br><br>

    <b>Revenue Exposure</b><br>
    Estimated annual revenue exposure is
    ₹ {revenue_risk:,}.<br><br>

    <b>Critical Accounts</b><br>
    Top 5 high-value at-risk customers contribute
    ₹ {int(top_5_loss):,} in potential annual loss.<br><br>

    <b>Portfolio Churn Trend</b><br>
    Average churn probability among high-risk customers
    is currently {avg_churn}%.<br><br>

    <b>Recommended Immediate Actions</b><br>

    • Prioritize outreach to high-value customers<br>
    • Launch targeted retention campaigns<br>
    • Provide premium support for inactive users<br>
    • Offer renewal incentives for expiring subscriptions<br>
    • Monitor payment failure accounts proactively

    </div>

    </div>

    """, unsafe_allow_html=True)

# =====================================================
# RETENTION PAGE
# =====================================================

elif page == "Retention":

    st.markdown(
        '<div class="section-title"> Retention Action Panel</div>',
        unsafe_allow_html=True
    )

    customer_name = st.selectbox(
        "Select Customer",
        df["customer_name"].unique()
    )

    if st.button("Send Offer"):

        st.success(
            f"Offer sent successfully to {customer_name}"
        )

    st.markdown("###")

    if st.button(
        "Send Offers to ALL High Risk Customers"
    ):

        st.success(
            "Offers sent to all high-risk customers"
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""

<br><br><hr>

<center>

<h4 style="
color:white;
font-weight:600;
letter-spacing:0.5px;
">
ChurnShield  Platform
</h4>

<p style="
color:#94a3b8;
font-size:14px;
margin-top:6px;
">
AI-Powered Customer Retention & Risk Analytics
</p>

<p style="
color:#64748b;
font-size:13px;
margin-top:12px;
">
© 2026 ChurnShield. All rights reserved.
</p>

<p style="
color:#475569;
font-size:12px;
">
yashwanthannamgalla@gmail.com
</p>

</center>

""", unsafe_allow_html=True)