from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SkillViewSet,
    CareerPathViewSet,
    UserSkillViewSet,
    LearningResourceViewSet,
    InterviewQuestionViewSet,
    UserProfileViewSet,
    UserProgressViewSet,
    RecommendationViewSet,
)

router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'career-paths', CareerPathViewSet)
router.register(r'user-skills', UserSkillViewSet, basename='user-skill')
router.register(r'learning-resources', LearningResourceViewSet)
router.register(r'interview-questions', InterviewQuestionViewSet)
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')
router.register(r'user-progress', UserProgressViewSet, basename='user-progress')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]
