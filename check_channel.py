import os
import sys
import pickle
import googleapiclient.discovery

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def check():
    token_file = "token_manage.json"
    if not os.path.exists(token_file):
        print("Token not found.")
        return

    with open(token_file, 'rb') as token:
        credentials = pickle.load(token)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    
    request = youtube.channels().list(mine=True, part="snippet")
    response = request.execute()
    
    if not response.get('items'):
        print("No channel found.")
        return

    channel = response['items'][0]['snippet']
    print("\n--- CHANNEL DETAILS ON YOUTUBE ---")
    print(f"Name: {channel.get('title')}")
    print(f"Handle: {channel.get('customUrl')}")
    print(f"Description: {channel.get('description')}")
    print("----------------------------------\n")

if __name__ == "__main__":
    check()
