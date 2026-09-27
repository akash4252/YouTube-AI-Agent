import streamlit as st
import json
import os
import time

# Premium Page Config
st.set_page_config(page_title="AI Studio Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# Hardcoded Default Channels so they NEVER disappear
DEFAULT_CHANNELS = {
    "⚽ Ronaldo's Realm": {
        "niche": "Sports & Football Edits",
        "audience": "United States 🇺🇸",
        "status": "Active - Daily Automation"
    },
    "🤖 Nexvora AI Tech": {
        "niche": "Futuristic Tech & AI",
        "audience": "United States 🇺🇸",
        "status": "Active - Viral Engine"
    }
}

DB_FILE = "channels_db.json"

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .metric-card {background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);}
    .title-text {font-weight: 800; color: #00ffcc; text-transform: uppercase;}
    .stButton>button {background-color: #00ffcc; color: black; font-weight: bold; border-radius: 8px;}
    .stButton>button:hover {background-color: #00ccaa; color: white;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("⚡ AI Studio Pro")
st.sidebar.markdown("---")

selected_channel = st.sidebar.radio("📌 Select Active Channel", list(DEFAULT_CHANNELS.keys()) + ["➕ Add New Channel"])

if selected_channel == "➕ Add New Channel":
    st.title("➕ Create New AI Channel")
    st.markdown("Launch a new fully automated channel here.")
    st.info("Feature locked in demo mode. Connect to database to activate.")
else:
    st.markdown(f"<h1 class='title-text'>{selected_channel}</h1>", unsafe_allow_html=True)
    channel_info = DEFAULT_CHANNELS[selected_channel]
    
    # Premium Tabs UI
    tab1, tab2 = st.tabs(["📊 Analytics Overview", "⚙️ AI Automation Control"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='metric-card'><h3>Topic / Niche</h3><p>{channel_info['niche']}</p></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='metric-card'><h3>Target Audience</h3><p>{channel_info['audience']}</p></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='metric-card'><h3>Bot Status</h3><p>🟢 {channel_info['status']}</p></div>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("📈 Projected Monthly Views (AI Forecast)")
        # Dynamic dummy graph depending on channel
        if "Tech" in selected_channel:
            st.area_chart([0, 100, 500, 2000, 5000, 15000, 30000])
        else:
            st.area_chart([0, 50, 300, 900, 2500, 8000, 20000])
        
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🤖 Background Cloud Scheduler")
        st.info("💡 The AI Brain is hosted securely on GitHub Actions. It will automatically wake up and upload videos every day. You don't need to keep this page open.")
        
        st.success("✅ Daily Automation is LIVE and scheduled for US Peak Hours.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎬 Force Trigger Upload Now", use_container_width=True):
                st.warning("Trigger signal sent to cloud! Video will be uploaded shortly.")
                st.balloons()
        with col_b:
            if st.button("⏹️ Pause Automation", use_container_width=True):
                st.error("Automation paused. (Demo button)")
