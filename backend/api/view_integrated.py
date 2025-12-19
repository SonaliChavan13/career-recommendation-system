from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services.adzuna_service import adzuna_service
from .services.coursera_service import CourseraService
from .services.youtube_service import YouTubeService
from .models import Skill, CareerPath, LearningResource
import json
from rest_framework.permissions import AllowAny
coursera_service = CourseraService()
youtube_service = YouTubeService()

class IntegratedCareerAnalysisView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, career_title):
        """Get comprehensive career analysis using external APIs"""
        
        # 1. Get market data for this career
        job_data = adzuna_service.search_jobs(
            what=career_title,
            where='us',
            max_results=20
        )
        
        # 2. Get salary data
        salary_data = adzuna_service.get_salary_data(
            job_title=career_title,
            location='us'
        )
        
        # 3. Extract required skills from job descriptions
        extracted_skills = adzuna_service.extract_skills_from_jobs(
            job_title=career_title,
            location='us',
            max_pages=2
        )
        
        # 4. Get learning resources for top skills
        learning_resources = []
        for skill, count in extracted_skills[:5]:
            # Coursera courses
            courses = coursera_service.search_courses(
                query=skill,
                max_results=5
            )
            
            # YouTube tutorials
            youtube_videos = youtube_service.search_educational_content(
                query=f"{skill} tutorial",
                max_results=5
            )
            
            learning_resources.append({
                'skill': skill,
                'job_count': count,
                'courses': courses,
                'videos': youtube_videos
            })
        
        # 5. Analyze job requirements
        jobs = job_data.get('results', [])[:10]
        common_requirements = []
        for job in jobs:
            if 'description' in job:
                desc = job['description'].lower()
                requirements = self._extract_requirements(desc)
                common_requirements.extend(requirements)
        
        # Count requirements
        from collections import Counter
        top_requirements = Counter(common_requirements).most_common(10)
        
        return Response({
            'career_title': career_title,
            'market_data': {
                'total_jobs': job_data.get('count', 0),
                'average_salary': salary_data.get('median', 0),
                'salary_range': {
                    'min': salary_data.get('min', 0),
                    'max': salary_data.get('max', 0)
                }
            },
            'required_skills': extracted_skills,
            'common_requirements': top_requirements,
            'learning_resources': learning_resources,
            'sample_jobs': jobs[:5]
        })
    
    def _extract_requirements(self, description):
        # Simple keyword extraction
        keywords = [
            'degree', 'bachelor', 'master', 'phd', 'experience',
            'years', 'certification', 'certified', 'knowledge of',
            'proficient in', 'strong understanding', 'familiar with'
        ]
        
        found = []
        for keyword in keywords:
            if keyword in description:
                found.append(keyword)
        
        return found

class AutoPopulateCareerView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Automatically populate career path data from external APIs"""
        career_title = request.data.get('title', 'Software Developer')
        
        try:
            # Get market data
            job_data = adzuna_service.search_jobs(
                what=career_title,
                where='us',
                max_results=50
            )
            
            # Extract skills
            extracted_skills = adzuna_service.extract_skills_from_jobs(
                job_title=career_title,
                location='us',
                max_pages=2
            )
            
            # Get salary data
            salary_data = adzuna_service.get_salary_data(career_title, 'us')
            
            # Create or update career path in database
            career, created = CareerPath.objects.update_or_create(
                title=career_title,
                defaults={
                    'description': f"Career path for {career_title} based on market data",
                    'average_salary': salary_data.get('median', 70000),
                    'future_growth': 15,  # Could be calculated from trends
                    'required_experience': '2-5 years'
                }
            )
            
            # Add skills to career path
            for skill_name, frequency in extracted_skills[:10]:
                # Get or create skill
                skill, _ = Skill.objects.get_or_create(
                    name=skill_name.capitalize(),
                    defaults={
                        'category': 'Technical',
                        'description': f"Skill extracted from {career_title} job market"
                    }
                )
                
                # Add to career path with proficiency level based on frequency
                proficiency = min(5, max(3, frequency // 10))  # Scale frequency to 3-5
                
                from .models import CareerPathSkill
                CareerPathSkill.objects.update_or_create(
                    career_path=career,
                    skill=skill,
                    defaults={
                        'proficiency_level': proficiency,
                        'is_core': proficiency >= 4
                    }
                )
            
            # Add learning resources
            for skill_name, frequency in extracted_skills[:5]:
                # Get courses
                courses = coursera_service.search_courses(skill_name, 3)
                
                for course in courses:
                    skill = Skill.objects.filter(name=skill_name.capitalize()).first()
                    if skill:
                        LearningResource.objects.update_or_create(
                            title=course['name'],
                            defaults={
                                'description': course.get('description', ''),
                                'resource_type': 'course',
                                'url': course['link'],
                                'skill': skill,
                                'difficulty': 'beginner',
                                'estimated_hours': 20,
                                'free': course.get('free', True)
                            }
                        )
            
            return Response({
                'success': True,
                'career_id': career.id,
                'skills_added': len(extracted_skills[:10]),
                'resources_added': len(extracted_skills[:5]) * 3,
                'message': f"Career path '{career_title}' populated successfully"
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)