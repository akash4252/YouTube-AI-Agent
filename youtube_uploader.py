import os
import sys
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Scopes needed to upload videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "client_secrets.json"
    token_file = "token.json"
    
    if not os.path.exists(client_secrets_file):
        print(f"[!] Error: {client_secrets_file} not found!")
        sys.exit(1)

    print("[*] Authenticating with YouTube...")
    credentials = None

    # Load existing credentials if available
    if os.path.exists(token_file):
        import pickle
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)

    # If no valid credentials, login and save them
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save credentials for next time
        import pickle
        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    video_file = "final_shorts.mp4"
    if not os.path.exists(video_file):
        print(f"[!] Error: {video_file} not found! Generate the video first.")
        sys.exit(1)

    print(f"[*] Uploading {video_file} to YouTube...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "17", # 17 = Sports
            "description": "5 Times Cristiano Ronaldo SHOCKED The World! 🤯🔥 Subscribe for daily CR7 magic! #ronaldo #cr7 #football #shorts",
            "title": "5 Times Cristiano Ronaldo SHOCKED The World! 🤯🔥",
            "tags": ["ronaldo", "cr7", "football", "shorts", "cristiano ronaldo", "highlights"]
          },
          "status": {
            "privacyStatus": "private" # Kept private for testing. Change to 'public' later.
          }
        },
        media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )
    
    try:
        response = request.execute()
        print("\n🎉 SUCCESS! Video Uploaded!")
        print(f"🔗 Video URL: https://www.youtube.com/watch?v={response['id']}")
    except googleapiclient.errors.HttpError as e:
        print(f"\n[!] An HTTP error {e.resp.status} occurred:\n{e.content}")

if __name__ == "__main__":
    main()
