import requests
import json
from django.conf import settings
from django.core.cache import cache

class CourseraService:
    BASE_URL = "https://api.coursera.org/api/courses.v1"
    
    def search_courses(self, query="python", max_results=10):
        cache_key = f"coursera_{query}_{max_results}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}"
            params = {
                'q': 'search',
                'query': query,
                'limit': max_results,
                'fields': 'description,primaryLanguages,specializations,partnerIds'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Transform data
            courses = []
            for course in data.get('elements', []):
                courses.append({
                    'id': course.get('id'),
                    'name': course.get('name'),
                    'slug': course.get('slug'),
                    'description': course.get('description'),
                    'languages': course.get('primaryLanguages', []),
                    'link': f"https://www.coursera.org/learn/{course.get('slug')}",
                    'free': self._check_if_free(course)
                })
            
            cache.set(cache_key, courses, 86400)  # 24 hours
            
            return courses
        except Exception as e:
            print(f"Coursera API error: {e}")
            return []
    
    def _check_if_free(self, course):
        # Simple check - many Coursera courses are free to audit
        return True
    
    def get_course_details(self, course_id):
        try:
            url = f"{self.BASE_URL}/{course_id}"
            response = requests.get(url, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Coursera details error: {e}")
            return {}