import os
from instagrapi import Client

def upload_to_instagram(video_path, caption, channel_type):
    print(f"\n[*] Preparing Instagram upload for {channel_type}...")
    
    # Load credentials based on channel
    if channel_type == "CR7":
        username = os.environ.get("IG_CR7_USER")
        password = os.environ.get("IG_CR7_PASS")
    elif channel_type == "TECH":
        username = os.environ.get("IG_TECH_USER")
        password = os.environ.get("IG_TECH_PASS")
    else:
        print("[!] Unknown channel type.")
        return

    if not username or not password:
        print(f"[!] Instagram credentials for {channel_type} missing in GitHub Secrets. Skipping IG upload.")
        return

    try:
        cl = Client()
        # To avoid login issues on the cloud, delay slightly
        print(f"[*] Logging into Instagram account: {username} ...")
        cl.login(username, password)
        
        print(f"[*] Uploading Reel to Instagram...")
        # Upload video as a Reel (clip)
        cl.clip_upload(video_path, caption)
        print(f"✅ SUCCESS: Reel successfully uploaded to Instagram (@{username})!")
        
    except Exception as e:
        print(f"[!] Instagram Upload Failed: {e}")
