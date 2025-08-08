# =================== backend/scrape_creator.py ===================
import asyncio
from typing import Dict, List
import json
import random

async def scrape_instagram_profile(username: str, posts_limit: int = 12) -> Dict:
    try:
        # Mock data for demo - replace with actual Instagram API integration
        profile_data = {
            "username": username,
            "full_name": f"{username.title()} Profile",
            "biography": "Sample bio for analysis",
            "followers": random.randint(10000, 100000),
            "following": random.randint(500, 2000),
            "posts": [
                {
                    "id": f"{i}",
                    "image_url": f"https://picsum.photos/400/400?random={i}",
                    "caption": f"Sample post caption {i} with hashtags #brand #style #content",
                    "likes": random.randint(500, 2000),
                    "comments": random.randint(20, 150),
                    "timestamp": f"2025-08-{8-i:02d}T{10+i}:00:00Z"
                }
                for i in range(min(posts_limit, 12))
            ]
        }
        
        return profile_data
    except Exception as e:
        print(f"Error scraping profile: {e}")
        return {"error": str(e)}

def scrape_instagram_profile_sync(username: str):
    return asyncio.run(scrape_instagram_profile(username))

if __name__ == "__main__":
    result = scrape_instagram_profile_sync("nasa")
    print(json.dumps(result, indent=2))
