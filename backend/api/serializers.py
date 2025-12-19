from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        # Check if passwords match
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check if email already exists
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        # Check if username already exists
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        
        return attrs
    
    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class CareerPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPath
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSkillSerializer(serializers.ModelSerializer):
    skill_details = SkillSerializer(source='skill', read_only=True)
    
    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_details', 'proficiency_level', 'years_of_experience']

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = '__all__'

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = '__all__'

class UserProgressSerializer(serializers.ModelSerializer):
    resource_details = LearningResourceSerializer(source='resource', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    career_path_details = CareerPathSerializer(source='career_path', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = '__all__'

class CareerPathDetailSerializer(serializers.ModelSerializer):
    required_skills = serializers.SerializerMethodField()
    
    class Meta:
        model = CareerPath
        fields = '__all__'
    
    def get_required_skills(self, obj):
        skills = CareerPathSkill.objects.filter(career_path=obj)
        return CareerPathSkillSerializer(skills, many=True).data

class CareerPathSkillSerializer(serializers.ModelSerializer):
    skill_details = SkillSerializer(source='skill', read_only=True)
    
    class Meta:
        model = CareerPathSkill
        fields = ['skill', 'skill_details', 'proficiency_level', 'is_core']