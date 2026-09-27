import os
import sys
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "client_secrets.json"
    token_file = "token_nexvora.json" # SEPARATE TOKEN FOR TECH CHANNEL
    
    if not os.path.exists(client_secrets_file):
        print(f"[!] Error: {client_secrets_file} not found!")
        sys.exit(1)

    print("[*] Authenticating with YouTube for Tech Channel...")
    credentials = None

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=0)
        
        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    video_file = "final_shorts_tech.mp4"
    if not os.path.exists(video_file):
        print(f"[!] Error: {video_file} not found!")
        sys.exit(1)

    print(f"[*] Uploading {video_file} to Nexvora AI Tech...")
    
    request_body = {
        "snippet": {
            "title": "The Future of AI is HERE! 🤖 #shorts #tech #ai",
            "description": "Welcome to Nexvora AI Tech! Subscribe for the best AI news, future tech, and tutorials. #artificialintelligence #futuretech #nexvora",
            "tags": ["ai", "technology", "artificial intelligence", "tech", "nexvora", "future", "shorts"],
            "categoryId": "28" # Science & Technology
        },
        "status": {
            "privacyStatus": "private", # Keeping it private for review
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    try:
        response = request.execute()
        print("\n🎉 SUCCESS! Tech Video Uploaded!")
        print(f"🔗 Video URL: https://www.youtube.com/watch?v={response['id']}")
    except googleapiclient.errors.HttpError as e:
        print(f"\n[!] An HTTP error occurred: {e}")

if __name__ == "__main__":
    main()
