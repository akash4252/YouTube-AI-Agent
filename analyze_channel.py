import sys
import json

try:
    import yt_dlp
except ImportError:
    print("yt_dlp not found. Please install it using: pip install yt-dlp")
    sys.exit(1)

# Fix Windows encoding issue for emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_channel(channel_url):
    print(f"[*] AI Agent is analyzing the channel: {channel_url} ...\n")
    
    # yt-dlp options to extract video metadata quickly without downloading videos
    ydl_opts = {
        'extract_flat': True,
        'playlistend': 10,  # Fetch data of the last 10 videos
        'quiet': True,
        'no_warnings': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
            
            channel_name = info.get('uploader') or info.get('title') or 'Unknown'
            channel_desc = info.get('description', '')
            entries = info.get('entries', [])

            print("========================================")
            print(f"📺 Channel Name: {channel_name}")
            if channel_desc:
                print(f"📝 Description: {channel_desc[:200]}...")
            print("========================================\n")

            print("🔍 Recent Videos Found:")
            video_data_for_ai = []
            
            for i, entry in enumerate(entries):
                title = entry.get('title', 'Unknown')
                views = entry.get('view_count', 'N/A')
                print(f"  {i+1}. {title} (Views: {views})")
                video_data_for_ai.append({"title": title, "views": views})

            print("\n========================================")
            print("🤖 AI Agent Task:")
            print("1. Read the above video titles.")
            print("2. Automatically determine the Channel Niche.")
            print("3. Identify Target Audience & Hashtags.")
            print("4. Generate a NEW video idea based on this data.")
            print("========================================")
            
            return {
                "channel_name": channel_name,
                "recent_videos": video_data_for_ai
            }

        except Exception as e:
            print(f"[!] Error analyzing channel: {e}")

if __name__ == "__main__":
    # Test URL or take from command line
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/@YouTubeCreators"
    analyze_channel(url)
