import os
print("🚀 Running Cloud Automation via GitHub Actions...")

try:
    print("=== Executing CR7 Automation ===")
    os.system("python video_creator.py")
    os.system("python youtube_uploader.py")
except Exception as e:
    print(f"CR7 Error: {e}")

try:
    print("=== Executing Tech Automation ===")
    os.system("python viral_tech_video.py")
except Exception as e:
    print(f"Tech Error: {e}")

print("✅ Cloud Automation complete for today!")
