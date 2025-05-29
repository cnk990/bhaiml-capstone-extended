import streamlit as st
import pandas as pd
import joblib
import os

# Streamlit page config
st.set_page_config(page_title="Gaming Trends 2024 Insights", layout="wide")
st.title("Gaming Trends 2024 Insights Dashboard")
st.markdown("Explore predictions and actionable insights using XGBoost and PDPs")

# stakeholder to feature mapping
stakeholder_map = {
    "Developers": ["scaled_daily_active_users_dau"],
    "PMs": [
        "purchases_per_session",
        "release_month_freq",
        "release_dayofweek_freq",
        "release_quarter_freq",
        "dau_bin_Very High",
        "dau_bin_Medium",
        "dau_bin_Low",
        "dau_bin_High"
    ],
    "Marketers": [
        "scaled_new_registrations",
        "stream_viewers_per_player",
        "scaled_social_media_mentions",
        "scaled_stream_viewership",
        "influencer_endorsements"
    ],
    "Designers": [
        "dau_x_duration",
        "scaled_session_duration_minutes",
        "engagement_level_High"
    ],
    "Publishers": [
        "scaled_ingame_purchases_",
        "top_genre_freq",
        "platform_freq"
    ]
}

# features to PDP titles mapping
titles = {
    'scaled_daily_active_users_dau': 'Developers – DAU Impact',
    'scaled_new_registrations': 'Marketers – New Player Growth',
    'dau_x_duration': 'Designers – Session Intensity',
    'scaled_ingame_purchases_': 'Publishers – In-Game Spend',
    'stream_viewers_per_player': 'Marketers – Stream Popularity per Player',
    'scaled_social_media_mentions': 'Marketers - Impact of Social Media Buzz on Revenue',
    'dau_bin_High': 'PMs – High DAU Tier’s Relationship with Monetization',
    'dau_bin_Low': 'PMs – Low DAU Tier and Monetization Behavior',
    'dau_bin_Medium': 'PMs – Medium DAU Tier Performance Insights',
    'dau_bin_Very High': 'PMs – Very High DAU Tier: Saturation or Scale?',
    'scaled_session_duration_minutes': 'Designers – Session Length Influence on Revenue',
    'purchases_per_session': 'PMs – Average Purchases per Session vs Monetization',
    'scaled_stream_viewership': 'Marketers – General Stream Viewership vs Revenue Trends',
    'engagement_level_High': 'Designers – High Engagement User Segment Impact',
    'release_month_freq': 'PMs – Seasonal Release Trends and Revenue Impact',
    'top_genre_freq': 'Publishers – Popular Genres and Monetization Potential',
    'release_dayofweek_freq': 'PMs – Day of Release Influence on Revenue Performance',
    'platform_freq': 'Publishers – Platform Distribution and Monetization',
    'influencer_endorsements': 'Marketers – Endorsement Count and Revenue Impact',
    'release_quarter_freq': 'PMs – Quarterly Release Patterns and Monetization Trends'

}

# sidebar for stakeholder selection
stakeholder = st.sidebar.selectbox(
    "Select Stakeholder Group",
    list(stakeholder_map.keys())
)

# load model and data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "pdp_insights/models", "random_search_rf_model.joblib")
model = joblib.load(model_path)

# load data
data_path = os.path.join(BASE_DIR, "pdp_insights/data", "enhanced_gaming_trends_data.csv")
df = pd.read_csv(data_path)

# pdp display for selected stakeholder
st.subheader(f"PDP Insights for {stakeholder}")
st.markdown("this section displays **PDP Interpretations** and **feature-level** impact for the selected stakeholder.")

for feature in stakeholder_map[stakeholder]:
    safe_feature = feature.replace(" ", "_").replace("/", "_")
    image_path = os.path.join("pdp_insights/frontend", "pdps", f"{safe_feature}.png")
    readable_title = titles.get(feature, feature)

    if os.path.exists(image_path):
        st.markdown(f"### {readable_title}")
        st.image(image_path, caption=f"PDP: {feature}", use_container_width=True)
        st.markdown("---")
    else:
        st.warning(f"No PDP found for feature: {feature}")
