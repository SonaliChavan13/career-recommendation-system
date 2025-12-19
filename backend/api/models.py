from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# =========================
# SKILL
# =========================
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('ai_ml', 'AI / Machine Learning'),
        ('data_science', 'Data Science'),
        ('web_dev', 'Web Development'),
        ('cloud_devops', 'Cloud & DevOps'),
        ('databases', 'Databases'),
        ('tools', 'Tools'),
        ('soft_skills', 'Soft Skills'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =========================
# CAREER PATH
# =========================
class CareerPath(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    average_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    future_growth = models.FloatField(help_text="Growth percentage")
    required_experience = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# =========================
# CAREER PATH SKILL MAPPING
# =========================
class CareerPathSkill(models.Model):
    career_path = models.ForeignKey(
        CareerPath, on_delete=models.CASCADE, related_name='required_skills'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_core = models.BooleanField(default=False)

    class Meta:
        unique_together = ('career_path', 'skill')

    def __str__(self):
        return f"{self.career_path.title} - {self.skill.name}"


# =========================
# USER PROFILE
# =========================
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    current_role = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    education_level = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# =========================
# USER SKILL
# =========================
class UserSkill(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='skills'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
    years_of_experience = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"


# =========================
# LEARNING RESOURCE
# =========================
class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ('course', 'Course'),
        ('book', 'Book'),
        ('tutorial', 'Tutorial'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('documentation', 'Documentation'),
    ]

    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    url = models.URLField()
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='resources'
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    estimated_hours = models.IntegerField()
    free = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# =========================
# INTERVIEW QUESTION
# =========================
class InterviewQuestion(models.Model):
    QUESTION_TYPES = [
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('situational', 'Situational'),
    ]

    career_path = models.ForeignKey(
        CareerPath, on_delete=models.CASCADE, related_name='interview_questions'
    )
    question = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    sample_answer = models.TextField()
    tips = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=20, choices=LearningResource.DIFFICULTY_LEVELS
    )

    def __str__(self):
        return f"{self.career_path.title} - {self.question[:40]}"


# =========================
# USER PROGRESS
# =========================
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(LearningResource, on_delete=models.CASCADE)
    progress_percentage = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'resource')

    def __str__(self):
        return f"{self.user.username} - {self.resource.title}"


# =========================
# RECOMMENDATION
# =========================
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    match_percentage = models.FloatField()
    skill_gaps = models.JSONField(default=list)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.career_path.title}"
