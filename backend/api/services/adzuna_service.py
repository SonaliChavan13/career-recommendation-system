import requests 
import json
from django.conf import settings
from django.core.cache import cache
from datetime import datetime, timedelta

class AdzunaService:
    BASE_URL = "http://api.adzuna.com/v1/api"
    
    def __init__(self):
        self.app_id = getattr(settings, '5dac6c1e', '')
        self.app_key = getattr(settings, 'c1a3bb7b4137b225a064f37819d0c1ca', '')
    
    def search_jobs(self, what="software developer", where="us", max_results=10):
        """Search for jobs by keyword and location"""
        cache_key = f"adzuna_jobs_{what}_{where}_{max_results}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/jobs/{where}/search/1"
            params = {
                'app_id': self.app_id,
                'app_key': self.app_key,
                'what': what,
                'results_per_page': max_results,
                'content-type': 'application/json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Cache for 1 hour
            cache.set(cache_key, data, 3600)
            
            return data
        except Exception as e:
            print(f"Adzuna API error: {e}")
            return {'results': []}
    
    def get_job_categories(self):
        """Get all job categories"""
        cache_key = "adzuna_categories"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/jobs/us/categories"
            params = {
                'app_id': self.app_id,
                'app_key': self.app_key,
                'content-type': 'application/json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            cache.set(cache_key, data, 86400)  # 24 hours
            
            return data
        except Exception as e:
            print(f"Adzuna categories error: {e}")
            return {'results': []}
    
    def get_salary_data(self, job_title="software developer", location="us"):
        """Get salary information for a job title"""
        cache_key = f"adzuna_salary_{job_title}_{location}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/jobs/{location}/salary_stats"
            params = {
                'app_id': self.app_id,
                'app_key': self.app_key,
                'title': job_title,
                'content-type': 'application/json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            cache.set(cache_key, data, 86400)  # 24 hours
            
            return data
        except Exception as e:
            print(f"Adzuna salary error: {e}")
            return {}
    
    def extract_skills_from_jobs(self, job_title="developer", location="us", max_pages=3):
        """Extract common skills from job descriptions"""
        all_skills = []
        
        for page in range(1, max_pages + 1):
            url = f"{self.BASE_URL}/jobs/{location}/search/{page}"
            params = {
                'app_id': self.app_id,
                'app_key': self.app_key,
                'what': job_title,
                'results_per_page': 50,
                'content-type': 'application/json'
            }
            
            try:
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                
                # Extract skills from job descriptions
                for job in data.get('results', []):
                    description = job.get('description', '').lower()
                    
                    # Simple skill extraction (you can enhance this)
                    tech_skills = [
                        'python', 'javascript', 'java', 'c++', 'react', 'angular',
                        'vue', 'node.js', 'django', 'flask', 'spring', 'sql',
                        'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git',
                        'linux', 'machine learning', 'data science', 'ai'
                    ]
                    
                    for skill in tech_skills:
                        if skill in description:
                            all_skills.append(skill)
                            
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
        
        # Count frequency and return top skills
        from collections import Counter
        skill_counts = Counter(all_skills)
        
        return skill_counts.most_common(20)

# Singleton instance
adzuna_service = AdzunaService()