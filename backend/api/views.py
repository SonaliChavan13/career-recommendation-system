from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg
from datetime import datetime

from .models import (
    Skill,
    CareerPath,
    CareerPathSkill,
    UserSkill,
    LearningResource,
    InterviewQuestion,
    UserProfile,
    UserProgress,
    Recommendation,
)
from .serializers import (
    SkillSerializer,
    CareerPathSerializer,
    CareerPathDetailSerializer,
    UserSkillSerializer,
    LearningResourceSerializer,
    InterviewQuestionSerializer,
    UserProfileSerializer,
    UserProgressSerializer,
    RecommendationSerializer,
)

# -------------------------------------------------
# HELPER: GET DEMO USER
# -------------------------------------------------
def get_demo_user():
    user, _ = User.objects.get_or_create(
        username="demo",
        defaults={"email": "demo@example.com"}
    )
    return user


# =================================================
# SKILLS
# =================================================
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category']


# =================================================
# CAREER PATHS
# =================================================
class CareerPathViewSet(viewsets.ModelViewSet):
    queryset = CareerPath.objects.all()
    serializer_class = CareerPathSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CareerPathDetailSerializer(instance)
        return Response(serializer.data)


# =================================================
# USER SKILLS (FIXED FOR DEMO USER)
# =================================================
class UserSkillViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        demo_user = get_demo_user()
        return UserSkill.objects.filter(user=demo_user)

    def perform_create(self, serializer):
        demo_user = get_demo_user()
        serializer.save(user=demo_user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def skill_gaps(self, request):
        demo_user = get_demo_user()
        recommendations = Recommendation.objects.filter(user=demo_user)

        gaps = []
        for rec in recommendations:
            gaps.append({
                "career_path": CareerPathSerializer(rec.career_path).data,
                "match_percentage": rec.match_percentage,
                "skill_gaps": rec.skill_gaps
            })

        return Response(gaps)


# =================================================
# LEARNING RESOURCES
# =================================================
class LearningResourceViewSet(viewsets.ModelViewSet):
    queryset = LearningResource.objects.all()
    serializer_class = LearningResourceSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'skill__name']


# =================================================
# INTERVIEW QUESTIONS
# =================================================
class InterviewQuestionViewSet(viewsets.ModelViewSet):
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewQuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def practice_session(self, request):
        questions = InterviewQuestion.objects.order_by('?')[:10]

        data = [
            {
                "id": q.id,
                "question": q.question,
                "difficulty": q.difficulty,
                "question_type": q.question_type,
                "career_path": q.career_path.title,
            }
            for q in questions
        ]

        return Response({
            "total_questions": len(data),
            "questions": data
        })


# =================================================
# USER PROFILE (DEMO USER)
# =================================================
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        demo_user = get_demo_user()
        profile, _ = UserProfile.objects.get_or_create(user=demo_user)
        return UserProfile.objects.filter(user=demo_user)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        demo_user = get_demo_user()

        skills_count = UserSkill.objects.filter(user=demo_user).count()
        completed_resources = UserProgress.objects.filter(
            user=demo_user, completed=True
        ).count()

        return Response({
            "username": demo_user.username,
            "skills_count": skills_count,
            "completed_resources": completed_resources,
        })


# =================================================
# USER PROGRESS
# =================================================
class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        demo_user = get_demo_user()
        return UserProgress.objects.filter(user=demo_user)

    def perform_create(self, serializer):
        demo_user = get_demo_user()
        serializer.save(user=demo_user)


# =================================================
# RECOMMENDATIONS (OPTIONAL)
# =================================================
class RecommendationViewSet(viewsets.ModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        demo_user = get_demo_user()
        return Recommendation.objects.filter(user=demo_user)
