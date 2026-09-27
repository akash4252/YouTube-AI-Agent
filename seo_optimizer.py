import random
from datetime import datetime

def get_seo_metadata(channel_type):
    year = datetime.now().year
    
    if channel_type == "CR7":
        titles = [
            "5 Times Cristiano Ronaldo SHOCKED The World! 🤯⚽",
            "CR7's Free Kick Was Pure Magic! 🐐🔥",
            "No One Can Defend Prime Ronaldo! 🚀 #cr7",
            "The Exact Moment Ronaldo Became The GOAT 🏆",
            "Cristiano Ronaldo's Speed is UNREAL! ⚡",
            "Why CR7 is Better Than Messi (Proof) 🤫⚽",
            "Ronaldo's Most Disrespectful Skills Ever! 🥶"
        ]
        desc = (
            "Witness the greatness of Cristiano Ronaldo! 🐐🔥 Subscribe for daily CR7 magic, rare goals, and legendary football edits.\n\n"
            "👉 Subscribe to Ronaldo's Realm for more!\n\n"
            "⚠️ Disclaimer: All clips are property of their respective owners. No copyright infringement intended.\n\n"
            "#cristianoronaldo #cr7 #football #realmadrid #soccer #ronaldoedits #goat #shorts #portugal #championsleague"
        )
        tags = [
            "cristiano ronaldo", "cr7", "football shorts", "soccer edits", 
            "real madrid", "portugal", "ronaldo goals", "cr7 skills", 
            "football highlights", "ronaldo vs messi", "sports shorts", 
            "viral football", "champions league", "cr7 edit", "goat"
        ]
        
    elif channel_type == "TECH":
        titles = [
            f"3 FREE AI Tools That Save HOURS! ({year}) 🤖",
            "This New AI Tool is ILLEGAL to know! 🤯",
            f"Top AI Secrets Nobody is Talking About in {year} 🚀",
            "How ChatGPT Just Changed The World (Again!) 😱",
            "Do NOT Learn Coding Before Watching This AI Video 💻",
            "The Scariest AI Technology Coming Soon... 🛑",
            "I Tried The Most Powerful AI And Here Is What Happened 😳"
        ]
        desc = (
            "Stay ahead of the curve with the latest AI and Technology trends! 🚀🤖 We uncover the most powerful free tools, secret AI hacks, and future tech updates.\n\n"
            "👉 Subscribe to Nexvora AI Tech to never miss an update!\n\n"
            "⚠️ Disclaimer: For educational purposes only.\n\n"
            "#ai #artificialintelligence #tech #technology #chatgpt #aitools #futuretech #shorts #innovation"
        )
        tags = [
            "ai tools", "artificial intelligence", "chatgpt", "technology trends", 
            "tech news", "future tech", "ai news", "free ai tools", 
            "tech shorts", "openai", "tech review", "viral tech", 
            "machine learning", "tech tips", "innovation"
        ]
        
    else:
        titles = ["Amazing Video! 🚀"]
        desc = "Subscribe for more amazing content! #shorts"
        tags = ["shorts", "viral", "trending"]

    return {
        "title": random.choice(titles),
        "description": desc,
        "tags": tags
    }
