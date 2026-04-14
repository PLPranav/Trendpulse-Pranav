import requests
import json
import os
import time
from datetime import datetime

CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM", "linux", "apple", "google", "web"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global", "police", "court", "world"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "player", "league", "championship", "football", "baseball", "olympics"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome", "medical", "nature"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming", "tv", "actor"]
}

headers = {"User-Agent": "TrendPulse/1.0"}

def fetch_trending_stories():
    all_collected_stories = []
    category_counts = {cat: 0 for cat in CATEGORIES}
    
    print("Fetching top story IDs...")
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        ids = requests.get(top_stories_url, headers=headers).json()[:500]
        print(f"Found {len(ids)} potential stories. Starting keyword scan...")
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return []

    for story_id in ids:
        if sum(category_counts.values()) >= 125:
            print("Target reached (125 stories). Stopping.")
            break
            
        try:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(item_url, headers=headers).json()
            
            if not story or 'title' not in story:
                continue
                
            title_text = story['title']
            title_lower = title_text.lower()
            
            for category, keywords in CATEGORIES.items():
                if category_counts[category] >= 25:
                    continue
                
                if any(kw.lower() in title_lower for kw in keywords):
                    story_data = {
                        "post_id": story.get("id"),
                        "title": title_text,
                        "category": category,
                        "score": story.get("score"),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().isoformat()
                    }
                    
                    all_collected_stories.append(story_data)
                    category_counts[category] += 1
                    
                    print(f"Found [{category}]: {title_text[:50]}...")
                    
                    time.sleep(2) 
                    break 
                    
        except Exception as e:
            print(f"Error fetching story {story_id}: {e}")
            continue

    return all_collected_stories

def save_data(stories):
    if not stories:
        print("No stories were collected. Check your keywords or internet connection.")
        return

    if not os.path.exists('data'):
        os.makedirs('data')
    
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    with open(filename, 'w') as f:
        json.dump(stories, f, indent=4)
    
    print("\n" + "="*30)
    print(f"SUCCESS: Collected {len(stories)} stories.")
    print(f"File saved to: {filename}")
    print("="*30)

if __name__ == "__main__":
    data = fetch_trending_stories()
    save_data(data)