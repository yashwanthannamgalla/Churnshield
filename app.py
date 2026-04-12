import streamlit as st
import pandas as pd
import model_utils as mu
import offers


# ---------- PAGE ----------

st.set_page_config(
    page_title="Retention Intelligence",
    layout="wide",
    page_icon="📊"
)

# ---------- LOAD ----------

data = mu.load_data()

model = mu.load_model()

data,X = mu.predict_churn(model,data)

feature_scores,top_feature = mu.get_feature_importance(
    model,
    X
)

# individual reasons
data["reason"] = mu.get_customer_reason(
    model,
    X
)

#revenue
data = mu.calculate_business_metrics(data)

# ---------- SEGMENT ----------

def segment(p):

    if p>0.8:
        return "High Risk"

    elif p>0.5:
        return "Medium Risk"

    else:
        return "Low Risk"


data["segment"] = data[
    "churn_probability"
].apply(segment)


# ---------- HEADER ----------

st.title("Customer Retention Dashboard")

st.caption(
"""
Identify at-risk customers  
take proactive retention actions
"""
)


# ---------- KPIs ----------

k1,k2,k3,k4 = st.columns(4)

k1.metric(
    "Customers",
    len(data)
)

k2.metric(
    "High Risk",
    len(data[data.segment=="High Risk"])
)

k3.metric(
    "Medium Risk",
    len(data[data.segment=="Medium Risk"])
)

k4.metric(
    "Low Risk",
    len(data[data.segment=="Low Risk"])
)


st.divider()



# =====================================================
# BUSINESS METRICS
# =====================================================

st.divider()

st.subheader("Business Impact Overview")


total_yearly_revenue = data[
    "yearly_revenue"
].sum()


high_risk = data[
    data.segment=="High Risk"
]


medium_risk = data[
    data.segment=="Medium Risk"
]


revenue_at_risk = (

    high_risk["yearly_revenue"].sum() +

    medium_risk["yearly_revenue"].sum()

)


retention_spending = (

    high_risk["retention_cost"].sum() +

    medium_risk["retention_cost"].sum()

)


potential_loss = (

    revenue_at_risk -

    retention_spending

)


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Total yearly revenue",
    f"₹ {int(total_yearly_revenue):,}"
)


c2.metric(
    "Revenue at risk",
    f"₹ {int(revenue_at_risk):,}"
)


c3.metric(
    "Estimated retention spending",
    f"₹ {int(retention_spending):,}"
)


c4.metric(
    "Potential loss",
    f"₹ {int(potential_loss):,}"
)


st.caption(
"""
"Estimated yearly revenue contribution, retention investment, and potential financial loss from customers predicted to churn."

"""
)



st.subheader("Financial Risk Comparison")

finance_df = pd.DataFrame({

    "metric":[

        "Revenue at risk",

        "Retention spending",

        "Potential loss"

    ],

    "amount":[

        revenue_at_risk,

        retention_spending,

        potential_loss

    ]

})

st.bar_chart(

    finance_df.set_index("metric")

)

# ---------- MAIN ----------

left,right = st.columns([2,1])


with left:

    st.subheader(
        "Customers needing attention"
    )

    top = data.sort_values(
        by="churn_probability",
        ascending=False
    )

    st.dataframe(

        top.head(20)[
            [
                "customer_id",
                "customer_name",
                "segment",
                "churn_probability",
                "reason"
            ]
        ],

        use_container_width=True,
        height=420
    )


with right:

    st.subheader("Main churn driver")

    st.info(top_feature)


    st.subheader("Typical retention action")

    st.success(

        offers.choose_offer(top_feature)

    )


    st.subheader("Probability summary")

    st.write(

        data["churn_probability"].describe()

    )


# ---------- CHARTS ----------

c1,c2 = st.columns(2)


with c1:

    st.subheader("Risk distribution")

    st.bar_chart(

        data["segment"].value_counts()

    )


with c2:

    st.subheader("Top churn factors")

    st.bar_chart(

        feature_scores.abs()
        .sort_values(ascending=False)
        .head(8)

    )


# ---------- FILTER ----------

st.divider()

st.subheader("Customer explorer")

seg = st.selectbox(

    "Segment",

    ["All","High Risk","Medium Risk","Low Risk"]

)


if seg!="All":

    filtered = data[
        data.segment==seg
    ]

else:

    filtered = data


st.dataframe(

    filtered[
        [
            "customer_id",
            "customer_name",
            "segment",
            "churn_probability",
            "reason"
        ]
    ],

    use_container_width=True
)


# ---------- DETAIL ----------

st.divider()

st.subheader("Customer lookup")

cid = st.number_input(
    "customer id",
    value=int(data.customer_id.min())
)


row = data[
    data.customer_id==cid
]


if not row.empty:

    st.write(row.T)



# =====================================================
# OFFER MANAGEMENT SYSTEM
# =====================================================

st.divider()

st.subheader("Retention Action Panel")

st.caption(
"Assign personalized offers inside platform"
)


# storage
if "active_offers" not in st.session_state:

    st.session_state.active_offers = {}


# ---------- send single ----------

st.markdown("### Send offer to one customer")

selected_customer = st.selectbox(

    "Customer",

    data["customer_name"]

)


if st.button("Send offer"):

    reason = data.loc[
        data.customer_name==selected_customer,
        "reason"
    ].values[0]


    offer_text = offers.choose_offer(reason)


    st.session_state.active_offers[
        selected_customer
    ] = offer_text


    st.success(
        f"Offer assigned to {selected_customer}"
    )


# ---------- send bulk ----------

st.markdown("### Send offers to all high-risk customers")


if st.button("Send offers to ALL high-risk customers"):

    high_risk = data[
        data.segment=="High Risk"
    ]


    for _,row in high_risk.iterrows():

        reason = row["reason"]

        offer_text = offers.choose_offer(reason)

        st.session_state.active_offers[
            row["customer_name"]
        ] = offer_text


    st.success(
        f"Offers assigned to {len(high_risk)} customers"
    )


# ---------- view assigned ----------

if st.session_state.active_offers:

    st.subheader("Active offers inside platform")


    offer_df = pd.DataFrame({

        "customer_name":

        list(st.session_state.active_offers.keys()),

        "assigned_offer":

        list(st.session_state.active_offers.values())

    })


    st.dataframe(
        offer_df,
        use_container_width=True
    )