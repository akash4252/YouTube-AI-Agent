import streamlit as st
import json
import urllib.request
import re

# YouTube Studio Theme Config
st.set_page_config(page_title="YouTube Studio AI", page_icon="▶️", layout="wide", initial_sidebar_state="expanded")

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

DEFAULT_CHANNELS = {
    "⚽ Ronaldo's Realm": {"handle": "@cr7realmofficial_c", "niche": "Sports"},
    "🤖 Nexvora AI Tech": {"handle": "@NexvoraAITech", "niche": "Tech"}
}

# YouTube Studio Custom CSS
st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp {background-color: #0f0f0f; color: #f1f1f1;}
    .css-1d391kg {background-color: #0f0f0f;}
    
    /* Top Header */
    .studio-header {font-size: 28px; font-weight: 700; color: #fff; margin-bottom: 20px; font-family: "Roboto", sans-serif;}
    
    /* YouTube Table */
    .yt-table {width: 100%; border-collapse: collapse; font-family: "Roboto", sans-serif; color: #fff; margin-top: 10px;}
    .yt-table th {text-align: left; padding: 12px 16px; border-bottom: 1px solid #3d3d3d; color: #aaa; font-weight: 500; font-size: 13px;}
    .yt-table td {padding: 12px 16px; border-bottom: 1px solid #3d3d3d; font-size: 14px; vertical-align: middle;}
    .yt-row:hover {background-color: #272727;}
    
    /* Video Cell */
    .vid-cell {display: flex; gap: 16px; align-items: flex-start;}
    .thumb-box {width: 60px; height: 106px; background-color: #222; border-radius: 4px; overflow: hidden; position: relative; flex-shrink: 0;}
    .thumb-box img {width: 100%; height: 100%; object-fit: cover;}
    .time-badge {position: absolute; bottom: 4px; right: 4px; background: rgba(0,0,0,0.8); color: #fff; font-size: 10px; font-weight: 500; padding: 2px 4px; border-radius: 4px;}
    
    .vid-text {display: flex; flex-direction: column; justify-content: center;}
    .vid-title {font-weight: 500; color: #fff; font-size: 14px; line-height: 20px;}
    .vid-desc {color: #aaa; font-size: 12px; margin-top: 4px;}
    
    /* Visibility Icon */
    .visibility-public {display: flex; align-items: center; gap: 6px; color: #2ba640;}
    .icon-globe {width: 16px; height: 16px; fill: currentColor;}
    </style>
""", unsafe_allow_html=True)

# Sidebar (Studio Menu)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>▶️ Studio</h2>", unsafe_allow_html=True)
    st.markdown("---")
    selected_channel = st.radio("Your channels", list(DEFAULT_CHANNELS.keys()))
    
    st.markdown("---")
    st.success("🟢 Background AI Bot: Active")

st.markdown("<div class='studio-header'>Channel content</div>", unsafe_allow_html=True)

# Fetch Data
channel_info = DEFAULT_CHANNELS[selected_channel]
subs, vids, latest_vid = get_live_stats(channel_info["handle"])

# Tabs matching Studio
tab1, tab2, tab3 = st.tabs(["Videos", "Shorts", "Live"])

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate HTML Table
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
                    <div class="vid-text">
                        <div class="vid-title">Automated AI Video</div>
                        <div class="vid-desc">Uploaded by AI Agent • #shorts</div>
                    </div>
                </div>
            </td>
            <td>
                <div class="visibility-public">
                    <svg class="icon-globe" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" fill="currentColor"/></svg>
                    Public
                </div>
            </td>
            <td>Today<br><span style="color:#aaa;font-size:12px;">Published</span></td>
            <td>-</td>
            <td>-</td>
        </tr>
        """
    
    html_code += "</table>"
    st.markdown(html_code, unsafe_allow_html=True)
    
    if not latest_vid:
        st.info("No Shorts found on this channel yet. AI is working on it!")

with tab1:
    st.markdown("### Videos")
    st.write(f"Total uploads on channel: {vids}")
    st.info("AI is currently set to generate Shorts only.")
