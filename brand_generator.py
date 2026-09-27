import json
import google.generativeai as genai
import sys
import os

def generate_channel_brand(reference_data, api_key):
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    # Use Gemini Flash for quick and creative generation
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an expert YouTube Strategist and Brand Creator.
    I am providing you with the metadata of a successful reference YouTube channel:
    {json.dumps(reference_data, indent=2)}

    Your task is to create a COMPLETELY NEW, UNIQUE, and AI-DRIVEN YouTube channel based on the same niche and target audience, but with its own unique identity.

    Please provide the output strictly in the following JSON format without any markdown code blocks (just the raw JSON):
    {{
        "new_channel_name": "A catchy and unique name for the new channel",
        "channel_description": "An engaging, SEO-optimized 'About' section description (2-3 paragraphs)",
        "logo_prompt": "A detailed DALL-E/Midjourney prompt to generate the channel's logo",
        "banner_prompt": "A detailed image generation prompt for the channel banner art",
        "first_video_title": "A highly clickable, viral title for the very first video",
        "first_video_script_outline": "A brief 3-point outline for the first video"
    }}
    """
    
    print("[*] AI is generating a brand new channel identity...")
    response = model.generate_content(prompt)
    
    try:
        # Try to parse the JSON response
        result_text = response.text.replace('```json', '').replace('```', '').strip()
        brand_data = json.loads(result_text)
        
        print("\n🎉 NEW AI CHANNEL CREATED! 🎉")
        print("========================================")
        print(f"📺 Channel Name: {brand_data['new_channel_name']}")
        print(f"📝 Description: {brand_data['channel_description']}")
        print(f"🎨 Logo Prompt: {brand_data['logo_prompt']}")
        print(f"🖼️ Banner Prompt: {brand_data['banner_prompt']}")
        print(f"🎬 First Video Title: {brand_data['first_video_title']}")
        print("========================================\n")
        
        return brand_data
    except Exception as e:
        print("Error parsing AI response. Raw output was:")
        print(response.text)
        return None

if __name__ == "__main__":
    # Test Data (Mock reference data if no real data is passed)
    sample_reference = {
        "channel_name": "Tech Burner",
        "recent_videos": [
            {"title": "Don't Buy This Smartphone!", "views": "2M"},
            {"title": "AI is changing the world", "views": "1.5M"}
        ]
    }
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY environment variable is not set. Please set it to run the AI generator.")
        sys.exit(1)
        
    generate_channel_brand(sample_reference, api_key)
