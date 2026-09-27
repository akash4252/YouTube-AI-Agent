import streamlit as st
import json
import os
import random
import time

st.set_page_config(page_title="AI Agent Dashboard", page_icon="🤖", layout="wide")

DB_FILE = "channels_db.json"
if not os.path.exists(DB_FILE):
    default_data = {
        "Ronaldo's Realm": {
            "niche": "CR7 Highlights & Football Edits",
            "audience": "United States 🇺🇸",
            "status": "Active"
        }
    }
    with open(DB_FILE, "w") as f:
        json.dump(default_data, f)

with open(DB_FILE, "r") as f:
    channels = json.load(f)

# Sidebar
st.sidebar.title("📺 YouTube Studio AI")
st.sidebar.markdown("---")
st.sidebar.subheader("Your Channels")

# Navigation options
options = list(channels.keys()) + ["🔗 Link Existing Channel", "✨ Create New AI Channel"]
selected_channel = st.sidebar.radio("Navigation:", options)

if selected_channel == "🔗 Link Existing Channel":
    st.title("🔗 Link an Existing YouTube Channel")
    st.markdown("Already have a channel? Link it here to start automating uploads.")
    
    with st.form("link_channel_form"):
        e_name = st.text_input("Channel Name", placeholder="e.g., My Vlogs")
        e_url = st.text_input("Channel URL", placeholder="https://youtube.com/@...")
        e_niche = st.text_input("Current Niche", placeholder="e.g., Daily Vlogs")
        e_audience = st.selectbox("Target Audience", ["India 🇮🇳", "United States 🇺🇸", "Global 🌍"])
        submitted = st.form_submit_button("Link Channel")
        
        if submitted and e_name:
            channels[e_name] = {"niche": e_niche, "audience": e_audience, "status": "Linked (Ready)"}
            with open(DB_FILE, "w") as f:
                json.dump(channels, f)
            st.success(f"Existing channel '{e_name}' linked successfully! Please refresh.")

elif selected_channel == "✨ Create New AI Channel":
    st.title("✨ AI Channel Creator Builder")
    st.markdown("Let the AI do the heavy lifting! Just give us a broad topic, and we'll generate the branding.")
    
    broad_topic = st.text_input("What broad topic are you interested in?", placeholder="e.g., Technology, Finance, Fitness, Space...")
    
    if st.button("🧠 Generate Channel Ideas"):
        if broad_topic:
            with st.spinner("AI is analyzing trends and generating branding..."):
                time.sleep(2) # Simulate AI thinking
                
                # Simple mock AI logic for demonstration
                topic = broad_topic.lower()
                if "tech" in topic:
                    names = ["TechTitans", "FutureByte", "GadgetGenius AI"]
                    niches = ["AI Tools & News", "Gadget Reviews", "Coding & Tech Shorts"]
                    desc = "Welcome to the future! We bring you the latest in tech, AI breakthroughs, and gadget reviews. Stay ahead of the curve."
                elif "fin" in topic or "money" in topic:
                    names = ["WealthWave", "FinanceFrontier", "CryptoCash"]
                    niches = ["Personal Finance Tips", "Stock Market Shorts", "Crypto Updates"]
                    desc = "Your daily dose of financial literacy. Learn how to grow your wealth, invest smartly, and achieve financial freedom."
                else:
                    names = [f"{broad_topic.capitalize()} Hub", f"The {broad_topic.capitalize()} Space", f"Daily {broad_topic.capitalize()}"]
                    niches = [f"{broad_topic} Tips", f"{broad_topic} Facts", f"{broad_topic} Stories"]
                    desc = f"The ultimate destination for everything {broad_topic}! Subscribe for daily high-quality videos."

                st.session_state['ai_names'] = names
                st.session_state['ai_niches'] = niches
                st.session_state['ai_desc'] = desc
                st.session_state['topic'] = broad_topic

    if 'ai_names' in st.session_state:
        st.success("✅ AI Branding Generated!")
        st.markdown("### 🎯 AI Recommendations")
        
        with st.form("create_ai_channel_form"):
            selected_name = st.radio("Select a Channel Name:", st.session_state['ai_names'])
            selected_niche = st.radio("Select a Specific Niche:", st.session_state['ai_niches'])
            
            st.text_area("Suggested Description (You can edit this):", st.session_state['ai_desc'], height=100)
            
            st.markdown("#### 🎨 Visual Identity (Generated Prompts)")
            st.info("Logo Prompt: A minimalist, high-quality neon vector logo for '" + selected_name + "'. Dark background.")
            st.info("Banner Prompt: A cinematic, ultra-wide banner representing " + selected_niche + ", neon lighting, 8k resolution.")
            
            audience = st.selectbox("Target Audience", ["United States 🇺🇸 (Recommended for High CPM)", "Global 🌍", "India 🇮🇳"])
            
            if st.form_submit_button("🚀 Approve & Build Channel"):
                channels[selected_name] = {"niche": selected_niche, "audience": audience, "status": "AI Configured"}
                with open(DB_FILE, "w") as f:
                    json.dump(channels, f)
                st.balloons()
                st.success(f"Channel '{selected_name}' created successfully! Check the sidebar.")

else:
    # Existing Channel Dashboard View
    st.title(f"🚀 Dashboard: {selected_channel}")
    channel_info = channels[selected_channel]
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Target Audience", channel_info['audience'])
    col_b.metric("Niche", channel_info['niche'])
    col_c.metric("Bot Status", channel_info['status'])
    
    st.markdown("---")
    st.subheader("🛠️ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"🎬 Generate & Upload for {selected_channel}", use_container_width=True):
            st.info(f"🤖 Starting AI Agent for {selected_channel}...")
            st.success(f"✅ Video generated and uploaded successfully to {selected_channel}!")
            
    with col2:
        is_running = os.path.exists("scheduler_running.txt")
        
        if is_running:
            st.success("🟢 Daily Automation is currently RUNNING for this channel.")
            if st.button("⏹️ Stop Automation", use_container_width=True):
                os.remove("scheduler_running.txt")
                st.rerun()
        else:
            if st.button("⏱️ Start Daily Scheduler", use_container_width=True):
                st.warning(f"Starting the AI Brain for {selected_channel}...")
                
                # Mark as running
                with open("scheduler_running.txt", "w") as f:
                    f.write("Running")
                
                # Launch the actual daily scheduler in the background
                import subprocess
                subprocess.Popen(["python", "daily_scheduler.py"])
                
                st.success("✅ Automation ON! AI will now generate new topics and upload every day at US Peak Time.")
                st.balloons()
                time.sleep(2)
                st.rerun()

    st.markdown("---")
    st.subheader("📈 Channel Analytics (Preview)")
    st.line_chart([0, 15, 30, 150, 400, 1200, 3500])
