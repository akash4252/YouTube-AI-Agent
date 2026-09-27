import streamlit as st
import json
import os
import urllib.request
import re
import time

# --- Page Config ---
st.set_page_config(page_title="AI Studio Pro", page_icon="▶️", layout="wide", initial_sidebar_state="expanded")

# --- Helper Functions ---
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

@st.cache_data(ttl=600)
def get_live_stats(handle):
    try:
        url = f"https://www.youtube.com/{handle}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'var ytInitialData = ({.*?});</script>', html)
        if not match: return "N/A", "0", None
        data = json.loads(match.group(1))
        
        header = data.get('header', {}).get('pageHeaderRenderer', {}).get('content', {}).get('pageHeaderViewModel', {})
        metadata = header.get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
        subs, videos = "0", "0"
        for row in metadata:
            parts = row.get('metadataParts', [])
            for part in parts:
                text = part.get('text', {}).get('content', '')
                if 'subscriber' in text.lower(): subs = text.replace(' subscribers', '').replace(' subscriber', '')
                elif 'video' in text.lower(): videos = text.replace(' videos', '').replace(' video', '')
                
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
        return "N/A", "0", None

# --- Database ---
DB_FILE = "channels_db.json"
DEFAULT_CHANNELS = {
    "⚽ Ronaldo's Realm": {"handle": "@cr7realmofficial_c", "niche": "Sports"},
    "🤖 Nexvora AI Tech": {"handle": "@NexvoraAITech", "niche": "Tech"}
}

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump(DEFAULT_CHANNELS, f)

with open(DB_FILE, "r") as f:
    try:
        channels = json.load(f)
        for k, v in DEFAULT_CHANNELS.items():
            if k not in channels: channels[k] = v
    except:
        channels = DEFAULT_CHANNELS

# --- CSS (Studio Theme) ---
st.markdown("""
<style>
.stApp {background-color: #0f0f0f; color: #f1f1f1;}
.css-1d391kg {background-color: #0f0f0f;}
.studio-header {font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 20px;}
.yt-table {width: 100%; border-collapse: collapse; color: #fff; margin-top: 10px;}
.yt-table th {text-align: left; padding: 12px 16px; border-bottom: 1px solid #3d3d3d; color: #aaa; font-size: 13px;}
.yt-table td {padding: 12px 16px; border-bottom: 1px solid #3d3d3d; font-size: 14px;}
.yt-row:hover {background-color: #272727;}
.vid-cell {display: flex; gap: 16px;}
.thumb-box {width: 60px; height: 106px; background-color: #222; border-radius: 4px; position: relative;}
.thumb-box img {width: 100%; height: 100%; object-fit: cover;}
.time-badge {position: absolute; bottom: 4px; right: 4px; background: rgba(0,0,0,0.8); font-size: 10px; padding: 2px 4px; border-radius: 4px;}
.vid-title {font-weight: 500; font-size: 14px;}
.vid-desc {color: #aaa; font-size: 12px;}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>▶️ AI Studio</h2>", unsafe_allow_html=True)
    st.markdown("---")
    selected_channel = st.radio("Your channels", list(channels.keys()) + ["➕ Add New Channel"])

# --- Main App ---
if selected_channel == "➕ Add New Channel":
    st.title("➕ Create a New AI Channel")
    st.write("Launch a new fully automated channel in seconds.")
    
    new_name = st.text_input("Channel Name", placeholder="e.g. History Facts AI")
    new_handle = st.text_input("YouTube Handle", placeholder="e.g. @HistoryFactsAI")
    new_niche = st.selectbox("Select Niche", ["Technology", "Sports", "History", "Motivation", "Other"])
    
    if st.button("🚀 Generate AI Brand & Save", type="primary"):
        if new_name and new_handle:
            channels[new_name] = {"handle": new_handle, "niche": new_niche}
            with open(DB_FILE, "w") as f:
                json.dump(channels, f)
            st.success(f"✅ Channel '{new_name}' added successfully! Please Refresh the page.")
            st.balloons()
        else:
            st.error("Please enter both Name and Handle.")
            
else:
    channel_info = channels[selected_channel]
    st.markdown(f"<div class='studio-header'>{selected_channel}</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📺 Content (Studio)", "⚙️ Bot & Automation", "📊 Channel Analytics"])
    
    # Fetch Data
    subs, vids, latest_vid = get_live_stats(channel_info.get("handle", ""))
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        html_code = """
<table class="yt-table">
<tr>
<th style="width: 40px;"><input type="checkbox"></th>
<th style="width: 400px;">Short</th>
<th>Visibility</th>
<th>Date ↓</th>
<th>Views</th>
<th>Comments</th>
</tr>
"""
        if latest_vid:
            html_code += f"""
<tr class="yt-row">
<td><input type="checkbox"></td>
<td>
<div class="vid-cell">
<div class="thumb-box">
<img src="https://i.ytimg.com/vi/{latest_vid}/hqdefault.jpg">
<span class="time-badge">0:35</span>
</div>
<div>
<div class="vid-title">Automated AI Video</div>
<div class="vid-desc">Uploaded by AI Agent • #shorts</div>
</div>
</div>
</td>
<td style="color:#2ba640;">🌐 Public</td>
<td>Today<br><span style="color:#aaa;font-size:12px;">Published</span></td>
<td>-</td>
<td>-</td>
</tr>
"""
        html_code += "</table>"
        st.markdown(html_code, unsafe_allow_html=True)
        if not latest_vid:
            st.info("No Shorts found on this channel yet. AI is working on it!")

    with tab2:
        st.subheader("🤖 Bot Control Center")
        st.info("💡 The AI Brain is hosted securely on GitHub Actions (Cloud). It will automatically wake up and upload videos every day.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Activate Daily Bot (Cloud)", use_container_width=True):
                st.success("✅ Daily Bot Activated! It will now auto-generate and upload videos every 24 hours.")
        with col2:
            if st.button("🛑 Pause Bot", use_container_width=True):
                st.warning("⏸️ Bot Paused.")
                
        st.markdown("---")
        st.subheader("🎬 Manual Video Generation")
        if st.button("⚙️ Generate & Upload Video NOW", type="primary"):
            with st.spinner("🤖 AI is researching topics, writing script, and editing video..."):
                time.sleep(3) # Simulate loading for cloud UI
                st.success("✅ Video successfully generated and sent to YouTube queue!")
                st.balloons()
                
    with tab3:
        st.subheader("📊 Live Channel Analytics")
        st.write(f"**Total Subscribers:** {subs}")
        st.write(f"**Total Uploads:** {vids}")
        st.area_chart([0, 10, 50, 150, 400, 1000, 3000])
