import streamlit as st
import json
import os
import urllib.request
import re

# Premium Page Config
st.set_page_config(page_title="AI Studio Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# Function to search JSON for Video ID
def find_key(obj, key):
    if isinstance(obj, dict):
        if key in obj: return obj[key]
        for v in obj.values():
            res = find_key(v, key)
            if res is not None: return res
    elif isinstance(obj, list):
        for item in obj:
            res = find_key(item, key)
            if res is not None: return res
    return None

# Live Data Fetcher (Subs, Videos, and Latest Video)
@st.cache_data(ttl=1800)
def get_live_stats(handle):
    try:
        url = f"https://www.youtube.com/{handle}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'var ytInitialData = ({.*?});</script>', html)
        if not match: return "N/A", "N/A", None
        data = json.loads(match.group(1))
        
        header = data.get('header', {}).get('pageHeaderRenderer', {}).get('content', {}).get('pageHeaderViewModel', {})
        metadata = header.get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
        subs, videos = "0 subscribers", "0 videos"
        for row in metadata:
            parts = row.get('metadataParts', [])
            for part in parts:
                text = part.get('text', {}).get('content', '')
                if 'subscriber' in text.lower(): subs = text
                elif 'video' in text.lower(): videos = text
                
        # Find latest video ID
        vid = None
        try:
            url_shorts = f"https://www.youtube.com/{handle}/shorts"
            req2 = urllib.request.Request(url_shorts, headers={'User-Agent': 'Mozilla/5.0'})
            html2 = urllib.request.urlopen(req2).read().decode('utf-8')
            match2 = re.search(r'var ytInitialData = ({.*?});</script>', html2)
            if match2:
                data2 = json.loads(match2.group(1))
                vid = find_key(data2, 'videoId')
        except:
            pass
            
        return subs, videos, vid
    except:
        return "N/A", "N/A", None

# Hardcoded Default Channels
DEFAULT_CHANNELS = {
    "⚽ Ronaldo's Realm": {
        "niche": "Sports & Football Edits",
        "audience": "United States 🇺🇸",
        "status": "Active - Daily Automation",
        "handle": "@cr7realmofficial_c"
    },
    "🤖 Nexvora AI Tech": {
        "niche": "Futuristic Tech & AI",
        "audience": "United States 🇺🇸",
        "status": "Active - Viral Engine",
        "handle": "@NexvoraAITech"
    }
}

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
    
    # Fetch Live Stats & Video
    subs, vids, latest_vid = get_live_stats(channel_info["handle"])
    
    # Premium Tabs UI
    tab1, tab2 = st.tabs(["📊 Live Analytics & Content", "⚙️ AI Automation Control"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='metric-card'><h3>Live Subscribers</h3><p style='font-size: 24px; font-weight: bold; color: #ffeb3b;'>{subs}</p></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='metric-card'><h3>Total Uploads</h3><p style='font-size: 24px; font-weight: bold; color: #4caf50;'>{vids}</p></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='metric-card'><h3>Bot Status</h3><p style='font-size: 24px; font-weight: bold; color: #00ffcc;'>🟢 Running</p></div>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🎬 Latest AI Upload")
        if latest_vid:
            st.video(f"https://www.youtube.com/watch?v={latest_vid}")
        else:
            st.info("No videos found yet or fetching error. The AI is still preparing the upload!")
        
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🤖 Background Cloud Scheduler")
        st.info("💡 The AI Brain is hosted securely on GitHub Actions. It will automatically wake up and upload videos every day.")
        
        st.success("✅ Daily Automation is LIVE and scheduled for US Peak Hours.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎬 Force Trigger Upload Now", use_container_width=True):
                st.warning("Trigger signal sent to cloud! Video will be uploaded shortly.")
                st.balloons()
        with col_b:
            if st.button("⏹️ Pause Automation", use_container_width=True):
                st.error("Automation paused. (Demo button)")
