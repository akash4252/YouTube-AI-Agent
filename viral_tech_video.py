import os
import sys
import asyncio
import edge_tts
import PIL.Image
from PIL import ImageDraw, ImageFont

if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import *

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VOICE = "en-US-ChristopherNeural"
OUTPUT_VIDEO = "viral_shorts_tech.mp4"
AUDIO_FILE = "voiceover_viral.mp3"
THUMBNAIL_IMG = r"C:\Users\Admin\.gemini\antigravity\brain\6dfa25b6-ecc2-4d0b-a5b6-71c9d69d1942\viral_ai_thumbnail_1790511382647.jpg"

SCRIPT = """
Stop scrolling! If you are not using AI in 2026, you are already left behind.
Artificial Intelligence is no longer just a trend, it is a global takeover.
From generating hyper-realistic videos to writing thousands of lines of code in seconds.
Subscribe to Nexvora A.I. Tech to learn how to survive and thrive in the matrix!
"""

async def generate_voiceover():
    print(f"[*] Generating Viral AI Voiceover...")
    communicate = edge_tts.Communicate(SCRIPT, VOICE)
    await communicate.save(AUDIO_FILE)
    print(f"[+] Voiceover saved successfully!")

def create_viral_video():
    print("[*] Assembling the Viral Video...")
    
    # Audio
    audio_clip = AudioFileClip(AUDIO_FILE)
    duration = audio_clip.duration
    
    try:
        # Check if video exists, if not, download it dynamically (for Cloud)
        import glob
        video_file = None
        for ext in ["tech_source.mp4", "tech_source.f625.mp4", "tech_source.f399.mp4", "tech_source.f401.mp4"]:
            if os.path.exists(ext):
                video_file = ext
                break
                
        if not video_file:
            print("[*] Background video missing. Downloading dynamically for Cloud...")
            os.system('python -m yt_dlp -f "bestvideo[ext=mp4]/best[ext=mp4]" -o "tech_source.mp4" "ytsearch1:technology cyber futuristic background 4k loop"')
            video_file = "tech_source.mp4"
            
        print(f"[*] Using background video: {video_file}")
        bg_clip = VideoFileClip(video_file)
    except Exception as e:
        print(f"[!] Background video error: {e}")
        from moviepy.editor import ColorClip
        bg_clip = ColorClip(size=(1080, 1920), color=(15, 15, 30)).set_duration(duration)

    from moviepy.video.fx.all import loop, crop
    (w, h) = bg_clip.size
    target_w = h * 9 / 16
    bg_clip = crop(bg_clip, width=target_w, height=h, x_center=w / 2)
    bg_clip = bg_clip.resize(height=1920, width=1080)
    bg_clip = loop(bg_clip, duration=duration).set_opacity(0.4) # Darken background a bit
    
    # Solid black background underneath to make the 0.4 opacity work well
    solid_bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(duration)
    
    # Viral AI Image Overlay (Center)
    try:
        ai_image = ImageClip(THUMBNAIL_IMG)
        ai_image = ai_image.resize(width=900) # Big in the center
        ai_image = ai_image.set_position(("center", 200)).set_duration(duration)
        
        # Add a pop-in effect (Start at 0.1 to avoid width=0 error)
        def pop_in(t):
            if t < 0.5:
                scale = (t * 2)
                return max(scale, 0.01)
            return 1.0
            
        ai_image = ai_image.resize(pop_in)
    except Exception as e:
        print(f"Image error: {e}")
        ai_image = None
        
    # Create Text Overlay using Pillow (Guaranteed to work without ImageMagick)
    text_img_path = "viral_text.png"
    img = PIL.Image.new("RGBA", (1080, 500), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Using default font but very large by drawing scaled or if a truetype font is available
    try:
        # Try to use a thick Windows font
        font = ImageFont.truetype("impact.ttf", 150)
    except:
        font = ImageFont.load_default()
        
    text1 = "AI IN 2026"
    text2 = "IS SCARY..."
    
    # Draw outline/shadow for visibility
    shadow_color = "black"
    main_color = "yellow"
    
    # We just center the text manually
    draw.text((205, 55), text1, font=font, fill=shadow_color)
    draw.text((200, 50), text1, font=font, fill=main_color)
    
    draw.text((155, 255), text2, font=font, fill=shadow_color)
    draw.text((150, 250), text2, font=font, fill="white")
    
    img.save(text_img_path)
    
    text_clip = ImageClip(text_img_path).set_position(("center", 1300)).set_duration(duration)
    
    # Composite all layers
    layers = [solid_bg, bg_clip]
    if ai_image:
        layers.append(ai_image)
    layers.append(text_clip)
        
    video = CompositeVideoClip(layers)
    video = video.set_audio(audio_clip)

    print(f"[*] Rendering VIRAL tech video to {OUTPUT_VIDEO}...")
    video.write_videofile(OUTPUT_VIDEO, fps=30, codec="libx264", audio_codec="aac", logger=None)
    print(f"\n🎉 Viral Video successfully rendered!")

def main():
    asyncio.run(generate_voiceover())
    create_viral_video()

if __name__ == "__main__":
    main()
