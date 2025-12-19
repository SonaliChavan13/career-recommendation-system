from django.core.management.base import BaseCommand
from api.models import Skill, CareerPath, LearningResource, InterviewQuestion


class Command(BaseCommand):
    help = "Seed initial data for the Career Recommendation System"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding data...")

        # =========================
        # SKILLS
        # =========================
        skills_data = [
            ("Python", "programming", "General purpose programming language"),
            ("JavaScript", "programming", "Web development language"),
            ("React", "web_dev", "Frontend library"),
            ("Django", "web_dev", "Backend framework"),
            ("Machine Learning", "ai_ml", "ML concepts and algorithms"),
            ("SQL", "databases", "Database querying language"),
            ("AWS", "cloud_devops", "Cloud computing platform"),
            ("Git", "tools", "Version control system"),
            ("Communication", "soft_skills", "Professional communication skills"),
        ]

        skills = {}
        for name, category, description in skills_data:
            skill, _ = Skill.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": description,
                },
            )
            skills[name] = skill

        self.stdout.write("✅ Skills seeded")

        # =========================
        # CAREER PATHS
        # =========================
        career_paths_data = [
            ("Full Stack Developer", "Frontend and backend development"),
            ("Backend Developer", "Server-side application development"),
            ("Data Scientist", "Data analysis and machine learning"),
            ("Machine Learning Engineer", "Production ML systems"),
        ]

        career_paths = {}
        for title, description in career_paths_data:
            career, _ = CareerPath.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "future_growth": 20,
                    "required_experience": "1–3 years",
                },
            )
            career_paths[title] = career

        self.stdout.write("✅ Career paths seeded")

        # =========================
        # LEARNING RESOURCES
        # =========================
        resources_data = [
            (
                "Python Basics",
                "Learn Python from scratch",
                "course",
                "https://www.coursera.org/learn/python",
                "Python",
            ),
            (
                "React Basics",
                "Introduction to React",
                "course",
                "https://www.coursera.org/learn/front-end-react",
                "React",
            ),
            (
                "Django Fundamentals",
                "Backend development with Django",
                "course",
                "https://www.coursera.org/learn/django-for-everybody",
                "Django",
            ),
            (
                "Machine Learning Basics",
                "Introduction to Machine Learning",
                "course",
                "https://www.coursera.org/learn/machine-learning",
                "Machine Learning",
            ),
            (
                "Data Science Basics",
                "Introduction to data science concepts",
                "course",
                "https://www.coursera.org/learn/what-is-datascience",
                "Machine Learning",
            ),
            (
                "Git & GitHub Essentials",
                "Version control with Git and GitHub",
                "course",
                "https://www.udemy.com/course/git-and-github-crash-course/",
                "Git",
            ),
            (
                "SQL for Beginners",
                "Learn SQL for data analysis",
                "course",
                "https://www.coursera.org/learn/sql-for-data-science",
                "SQL",
            ),
            (
                "AWS Cloud Practitioner Essentials",
                "Introduction to AWS cloud services",
                "course",
                "https://explore.skillbuilder.aws/learn/course/134/aws-cloud-practitioner-essentials",
                "AWS",
            ),
            (
                "Communication Skills",
                "Improve professional communication skills",
                "course",
                "https://www.coursera.org/learn/wharton-communication-skills",
                "Communication",
            ),
        ]

        for title, description, rtype, url, skill_name in resources_data:
            LearningResource.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "resource_type": rtype,
                    "url": url,
                    "skill": skills[skill_name],
                    "difficulty": "beginner",
                    "estimated_hours": 10,
                    "free": True,
                },
            )

        self.stdout.write("✅ Learning resources seeded")

        # =========================
        # INTERVIEW QUESTIONS
        # =========================
        questions_data = [
            (
                "Full Stack Developer",
                "Explain the difference between frontend and backend.",
                "technical",
            ),
            (
                "Backend Developer",
                "What is REST API and why is it used?",
                "technical",
            ),
            (
                "Data Scientist",
                "What is overfitting in machine learning?",
                "technical",
            ),
            (
                "Machine Learning Engineer",
                "Explain bias vs variance tradeoff.",
                "technical",
            ),
        ]

        for career_title, question, qtype in questions_data:
            InterviewQuestion.objects.get_or_create(
                question=question,
                defaults={
                    "career_path": career_paths[career_title],
                    "question_type": qtype,
                    "sample_answer": "Sample answer for interview preparation.",
                    "difficulty": "beginner",
                },
            )

        self.stdout.write("✅ Interview questions seeded")

        self.stdout.write(self.style.SUCCESS("🎉 Database seeding completed successfully!"))
