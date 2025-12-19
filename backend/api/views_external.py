from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services.adzuna_service import adzuna_service
import json

class ExternalJobDataView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get job market data for a specific role"""
        job_title = request.query_params.get('title', 'software developer')
        location = request.query_params.get('location', 'us')
        max_results = request.query_params.get('max_results', 10)
        
        try:
            # Get job listings
            job_data = adzuna_service.search_jobs(
                what=job_title,
                where=location,
                max_results=int(max_results)
            )
            
            # Get salary data
            salary_data = adzuna_service.get_salary_data(
                job_title=job_title,
                location=location
            )
            
            # Extract skills from job descriptions
            extracted_skills = adzuna_service.extract_skills_from_jobs(
                job_title=job_title,
                location=location,
                max_pages=2
            )
            
            return Response({
                'success': True,
                'job_listings': job_data.get('results', [])[:10],
                'salary_info': salary_data,
                'extracted_skills': extracted_skills,
                'total_jobs': job_data.get('count', 0)
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarketTrendsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get market trends for different career paths"""
        categories = adzuna_service.get_job_categories()
        
        # Analyze trends for top categories
        trends = []
        for category in categories.get('results', [])[:5]:
            tag = category.get('tag', '')
            label = category.get('label', '')
            
            # Get job count for this category
            job_data = adzuna_service.search_jobs(
                what=label,
                where='us',
                max_results=1
            )
            
            trends.append({
                'category': label,
                'tag': tag,
                'job_count': job_data.get('count', 0),
                'average_salary': 0  # You can enhance this
            })
        
        return Response({
            'success': True,
            'trends': trends,
            'total_categories': len(categories.get('results', []))
        })

class SkillDemandView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get demand for specific skills in the market"""
        skill = request.query_params.get('skill', 'python')
        
        # Search for jobs requiring this skill
        job_data = adzuna_service.search_jobs(
            what=skill,
            where='us',
            max_results=50
        )
        
        # Analyze job data
        jobs = job_data.get('results', [])
        total_jobs = job_data.get('count', 0)
        
        # Calculate average salary for these jobs
        salaries = []
        locations = {}
        
        for job in jobs:
            # Salary
            salary_min = job.get('salary_min')
            salary_max = job.get('salary_max')
            if salary_min and salary_max:
                salaries.append((salary_min + salary_max) / 2)
            
            # Location
            location = job.get('location', {}).get('display_name', 'Unknown')
            locations[location] = locations.get(location, 0) + 1
        
        avg_salary = sum(salaries) / len(salaries) if salaries else 0
        
        # Get common related skills
        related_skills = []
        for job in jobs[:10]:
            description = job.get('description', '').lower()
            common_skills = ['javascript', 'sql', 'aws', 'docker', 'react']
            for s in common_skills:
                if s in description and s != skill:
                    related_skills.append(s)
        
        # Count related skills
        from collections import Counter
        top_related = Counter(related_skills).most_common(5)
        
        return Response({
            'skill': skill,
            'total_jobs': total_jobs,
            'average_salary': round(avg_salary, 2),
            'top_locations': dict(Counter(locations).most_common(5)),
            'related_skills': top_related,
            'sample_jobs': jobs[:5]
        })