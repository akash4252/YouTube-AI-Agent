import os
import sys
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# We need the full YouTube scope to change channel settings
SCOPES = ["https://www.googleapis.com/auth/youtube"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "client_secrets.json"
    token_file = "token_manage.json" # Separate token for manage scope
    
    if not os.path.exists(client_secrets_file):
        print("[!] Error: client_secrets.json not found!")
        sys.exit(1)

    print("[*] Authenticating with YouTube (Full Access)...")
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

    print("[*] Fetching channel details...")
    request = youtube.channels().list(mine=True, part="brandingSettings,snippet")
    response = request.execute()
    
    if not response.get('items'):
        print("[!] No channel found for this account.")
        sys.exit(1)

    channel_id = response['items'][0]['id']
    print(f"[*] Found Channel ID: {channel_id}")
    
    print("[*] Updating Channel Name and Description...")
    update_request = youtube.channels().update(
        part="brandingSettings",
        body={
            "id": channel_id,
            "brandingSettings": {
                "channel": {
                    "title": "Ronaldo's Realm",
                    "description": "Dive into the unparalleled legacy of Cristiano Ronaldo. Ronaldo's Realm brings you HD highlights, legendary goals, unmatched skills, and untold stories of the GOAT. Subscribe for daily football magic! ⚽🔥 #cr7 #ronaldo #football"
                }
            }
        }
    )
    
    try:
        update_response = update_request.execute()
        print("\n🎉 SUCCESS! Channel name and description updated successfully!")
    except Exception as e:
        print(f"\n[!] Error updating channel: {e}")

if __name__ == "__main__":
    main()
