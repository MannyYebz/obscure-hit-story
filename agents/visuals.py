import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_stock_footage(query, num_videos=5):
    api_key = os.getenv("PEXELS_API_KEY")
    
    url = "https://api.pexels.com/videos/search"
    
    headers = {
        "Authorization": api_key
    }
    
    params = {
        "query": query,
        "per_page": num_videos,
        "orientation": "portrait"  # vertical for TikTok
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        videos = []
        
        for video in data["videos"]:
            # Get the best quality video file
            video_files = video["video_files"]
            best_file = max(video_files, key=lambda x: x.get("height", 0))
            videos.append({
                "url": best_file["link"],
                "width": best_file["width"],
                "height": best_file["height"]
            })
        
        print(f"Found {len(videos)} videos for query: {query}")
        return videos
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    # Test with a music-related query
    videos = fetch_stock_footage("vintage music studio 1960s", num_videos=3)
    for i, v in enumerate(videos):
        print(f"Video {i+1}: {v['width']}x{v['height']} - {v['url'][:60]}...")