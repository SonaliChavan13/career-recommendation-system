import requests 
import json
from django.conf import settings
from django.core.cache import cache

class YouTubeService:
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    def __init__(self):
        self.api_key = getattr(settings, 'YOUTUBE_API_KEY', '')
    
    def search_educational_content(self, query="python tutorial", max_results=10):
        cache_key = f"youtube_{query}_{max_results}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/search"
            params = {
                'part': 'snippet',
                'q': f"{query} tutorial",
                'type': 'video',
                'videoDuration': 'medium',  # Medium length videos (4-20 min)
                'maxResults': max_results,
                'key': self.api_key,
                'relevanceLanguage': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                videos.append({
                    'id': video_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'duration': '10-30 minutes',  # You can get actual duration with videos.list
                    'free': True
                })
            
            cache.set(cache_key, videos, 43200)  # 12 hours
            
            return videos
        except Exception as e:
            print(f"YouTube API error: {e}")
            return []