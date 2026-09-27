import os
import sys
import pickle
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    token_file = "token_nexvora.json"
    
    if not os.path.exists(token_file):
        print(f"[!] Error: {token_file} not found! Run initial login first.")
        sys.exit(1)

    print("[*] Using saved token for Tech Channel...")
    with open(token_file, 'rb') as token:
        credentials = pickle.load(token)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    video_file = "viral_shorts_tech.mp4"

    print(f"[*] Uploading VIRAL {video_file} to Nexvora AI Tech...")
    
    request_body = {
        "snippet": {
            "title": "Don't Ignore AI in 2026! 🤯 The Truth They Hide From You #shorts #ai #future",
            "description": "Artificial Intelligence is taking over. Are you prepared for the future? Subscribe to Nexvora AI Tech to stay updated with the latest in technology, ChatGPT, robotics, and the Matrix. #artificialintelligence #futuretech #nexvora #tech #scary",
            "tags": ["ai", "technology", "artificial intelligence", "tech", "nexvora", "future", "shorts", "matrix", "chatgpt"],
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public",  # Making it public right away so it can go viral!
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")

    from seo_optimizer import get_seo_metadata
    seo = get_seo_metadata("TECH")
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    try:
        response = request.execute()
        print("\n🎉 SUCCESS! VIRAL Tech Video Uploaded & PUBLISHED!")
        print(f"🔗 Video URL: https://www.youtube.com/watch?v={response['id']}")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")

if __name__ == "__main__":
    main()
