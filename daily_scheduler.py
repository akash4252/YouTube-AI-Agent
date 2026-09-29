import time
import subprocess
import datetime
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def print_log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def run_tech_channel():
    print_log("🤖 [1/3] Researching today's VIRAL AI Topic...")
    # The script will use LLM to fetch a fresh topic (e.g., "3 New AI Tools")
    print_log("🤖 [2/3] Writing dynamic script and generating Voiceover...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run(["python", "viral_tech_video.py"], env=env)
    print_log("🤖 [3/3] Uploading with unique SEO Tags...")
    subprocess.run(["python", "viral_uploader.py"], env=env)
    print_log("✅ Tech Viral Video Uploaded!")

def run_cr7_channel():
    print_log("⚽ [1/3] Finding a new legendary CR7 story or fact...")
    # The script will fetch a new Ronaldo fact/stat daily
    print_log("⚽ [2/3] Creating video with dynamic captions...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run(["python", "video_creator.py"], env=env)
    subprocess.run(["python", "youtube_uploader.py"], env=env)
    print_log("✅ CR7 Video Uploaded!")

print_log("🚀 MASTER AUTO-SCHEDULER ACTIVATED!")
print_log("Channels Configured: [1] Ronaldo's Realm, [2] Nexvora AI Tech")
print_log("Monitoring time for US Peak Hours (EST)...")

if __name__ == "__main__":
    while True:
        now = datetime.datetime.now()
        
        # Upload Tech at 03:30 AM IST (6:00 PM EST - Evening Peak)
        if now.hour == 3 and now.minute == 30:
            run_tech_channel()
            time.sleep(60) # Wait a minute to avoid double trigger
            
        # Upload CR7 at 04:30 AM IST (7:00 PM EST - Evening Peak)
        if now.hour == 4 and now.minute == 30:
            run_cr7_channel()
            time.sleep(60)
            
        time.sleep(30)
# In a real environment, this loop checks the time.
# We simulate the daemon running indefinitely.
while True:
    now = datetime.datetime.now()
    
    # Upload Tech at 03:30 AM IST (6:00 PM EST - Evening Peak)
    if now.hour == 3 and now.minute == 30:
        run_tech_channel()
        time.sleep(60) # Wait a minute to avoid double trigger
        
    # Upload CR7 at 04:30 AM IST (7:00 PM EST - Evening Peak)
    if now.hour == 4 and now.minute == 30:
        run_cr7_channel()
        time.sleep(60)
        
    time.sleep(30)
