import os
import google.generativeai as genai

def generate_viral_script(channel_type):
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Fallback list if API fails or key is missing
    if channel_type == "CR7":
        fallback = "Cristiano Ronaldo just broke another massive record! The GOAT is unstoppable. His latest performance is breaking the internet right now. Subscribe if you think CR7 is the best!"
    else:
        fallback = "Did you know this secret AI tool can save you 10 hours a week? It's completely free and nobody is talking about it yet. Subscribe to Nexvora AI for more secrets!"
        
    if not api_key:
        print("[!] GEMINI_API_KEY not found in environment. Using fallback script.")
        return fallback
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        if channel_type == "CR7":
            prompt = """You are a viral YouTube Shorts scriptwriter. 
            Write a highly engaging, energetic 30-second script about a crazy Cristiano Ronaldo (CR7) fact, match, or record. 
            Include a strong hook in the first sentence. Keep it under 50 words. Do not include stage directions, emojis, or hashtags, just the plain spoken text."""
        else:
            prompt = """You are a viral YouTube Tech Shorts scriptwriter. 
            Write a highly engaging, energetic 30-second script about a new AI tool, hidden website, or tech trend. 
            Include a strong hook in the first sentence. Keep it under 50 words. Do not include stage directions, emojis, or hashtags, just the plain spoken text."""
            
        response = model.generate_content(prompt)
        script = response.text.replace('*', '').replace('"', '').strip()
        print(f"[*] AI Generated Script ({channel_type}): {script}")
        return script
    except Exception as e:
        print(f"[!] AI Generation Failed: {e}")
        return fallback
