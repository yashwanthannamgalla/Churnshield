def choose_offer(feature):

    offer_map = {

        # engagement behaviour
        "app_opened":
        "We noticed you haven't opened the app much. Here are personalized features you might like.",

        "session_duration":
        "Discover quick tips to get more value in less time.",

        "avg_time_per_day":
        "Build a daily habit and unlock streak rewards.",

        "weekly_active_days":
        "Stay active this week and earn bonus benefits.",

        "features_used":
        "Explore hidden features that can improve your experience.",

        "search_count":
        "We found content tailored to your interests.",

        "notifications_clicked":
        "Customize notifications to get only relevant updates.",

        "referrals_made":
        "Invite friends and both of you get reward credits.",


        # experience
        "complaints_raised":
        "We’re sorry for the inconvenience. Our support team will contact you with priority assistance.",

        "support_chat_used":
        "Dedicated support is available to resolve your concerns faster.",

        "tickets_resolved":
        "We’re improving our service. Here is a small thank-you reward.",

        "feedback_given":
        "Share feedback and earn reward points.",

        "rating_given":
        "We’d love to improve your experience. Tell us how we can do better.",


        # inactivity
        "days_inactive":
        "We miss you! Check out what's new since your last visit.",

        "last_login_gap":
        "Come back and explore newly added features.",


        # subscription behaviour
        "last_subscription_days":
        "Renew your subscription to continue enjoying premium benefits.",

        "subscription_renewal_gap":
        "Renew today to continue uninterrupted service.",

        "plan_upgrade_count":
        "Unlock more value with advanced plan benefits.",

        "plan_downgrade_count":
        "We can help you get more value from your current plan.",

        "auto_renew_enabled":
        "Enable auto-renew for uninterrupted service.",


        # payment behaviour
        "payment_success":
        "Enjoy hassle-free payments with faster checkout options.",

        "payment_failures":
        "Update payment details for seamless transactions.",

        "refund_requests":
        "We’re improving our service experience for you."
    }


    return offer_map.get(
        feature,
        "Enjoy personalized benefits designed for you."
    )