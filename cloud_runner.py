import os
import sys

# Add this folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from daily_scheduler import run_cr7_channel, run_tech_channel

print("🚀 Running Cloud Automation via GitHub Actions...")

# In the cloud, we don't use while True. 
# GitHub Actions acts as our timer. It wakes up, runs this, and shuts down.

try:
    print("=== Executing CR7 Automation ===")
    run_cr7_channel()
except Exception as e:
    print(f"CR7 Error: {e}")

try:
    print("=== Executing Tech Automation ===")
    run_tech_channel()
except Exception as e:
    print(f"Tech Error: {e}")

print("✅ Cloud Automation complete for today!")
