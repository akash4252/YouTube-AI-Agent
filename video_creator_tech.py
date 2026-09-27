import os
import sys
import asyncio
import edge_tts
import PIL.Image

if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import *

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VOICE = "en-US-ChristopherNeural"
OUTPUT_VIDEO = "final_shorts_tech.mp4"
AUDIO_FILE = "voiceover_tech.mp3"

TECH_SCRIPT = """
Are you ready for the future? Artificial Intelligence is evolving faster than ever. 
In 2026, AI is not just a tool; it is your ultimate superpower. 
From writing complex code to creating hyper-realistic videos, the matrix is already here. 
Welcome to Nexvora A.I. Tech, where we bring you the latest breakthroughs and future tech. 
Subscribe now to stay ahead of the curve!
"""

async def generate_voiceover(text, output_file):
    print(f"[*] Generating Tech AI Voiceover...")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)
    print(f"[+] Voiceover saved successfully as {output_file}\n")

def create_video():
    print("[*] Assembling the Tech Video...")
    try:
        audio_clip = AudioFileClip(AUDIO_FILE)
        duration = audio_clip.duration
    except Exception as e:
        print(f"[!] Error loading audio: {e}")
        return

    print(f"[*] Audio duration is {duration:.2f} seconds.")
    
    try:
        # Check which file downloaded (merged or unmerged video part)
        video_file = "tech_source.mp4"
        if not os.path.exists(video_file) and os.path.exists("tech_source.f401.mp4"):
            video_file = "tech_source.f401.mp4"
        elif not os.path.exists(video_file) and os.path.exists("tech_source.f399.mp4"):
            video_file = "tech_source.f399.mp4"
        elif not os.path.exists(video_file):
            # Fallback if specific ID downloaded
            import glob
            files = glob.glob("tech_source.*.mp4")
            if files: video_file = files[0]
            
        print(f"[*] Using background video: {video_file}")
        video_clip = VideoFileClip(video_file)
        
        from moviepy.video.fx.all import loop, crop
        
        (w, h) = video_clip.size
        target_w = h * 9 / 16
        x_center = w / 2
        
        bg_clip = crop(video_clip, width=target_w, height=h, x_center=x_center)
        bg_clip = bg_clip.resize(height=1920, width=1080)
        bg_clip = loop(bg_clip, duration=duration)
    except Exception as e:
        print(f"[!] Error loading video clip: {e}")
        bg_clip = ColorClip(size=(1080, 1920), color=(10, 10, 50)).set_duration(duration)
    
    video = CompositeVideoClip([bg_clip])
    video = video.set_audio(audio_clip)

    print(f"[*] Rendering final tech video to {OUTPUT_VIDEO}...")
    video.write_videofile(OUTPUT_VIDEO, fps=30, codec="libx264", audio_codec="aac", logger=None)
    print(f"\n🎉 Tech Video successfully rendered: {os.path.abspath(OUTPUT_VIDEO)}")

def main():
    asyncio.run(generate_voiceover(TECH_SCRIPT, AUDIO_FILE))
    create_video()

if __name__ == "__main__":
    main()
