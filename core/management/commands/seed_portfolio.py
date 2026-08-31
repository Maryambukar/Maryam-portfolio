"""
Populates the database with the real, confirmed information you provided
(name, university, CGPA, Dean's List, secondary school, VS Code/GitHub/
Python, soft skills, and the two confirmed achievements). Nothing here is
invented — it's exactly what was in the master prompt and About copy.

Safe to re-run: uses get_or_create / update_or_create throughout.

Usage:
    python manage.py seed_portfolio
"""
from django.core.management.base import BaseCommand

from core.models import AcademicFact, EducationEntry, SiteOwner
from portfolio.models import Achievement, Skill, SkillCategory


class Command(BaseCommand):
    help = 'Seed the database with the real, confirmed portfolio content.'

    def handle(self, *args, **options):
        owner, _ = SiteOwner.objects.update_or_create(
            pk=1,
            defaults={
                'name': 'Maryam Bukar',
                'headline': 'Aspiring Data Scientist & Analyst / Software Developer',
                'bio': (
                    'I am a Data Science & Analytics student at the American '
                    'University of Nigeria (AUN), Yola, with a growing passion '
                    'for software development, data, and technology.'
                ),
                'university': 'American University of Nigeria (AUN)',
                'location': 'Yola, Nigeria',
            },
        )

        AcademicFact.objects.update_or_create(
            owner=owner,
            defaults={
                'degree_program': 'B.Sc. Data Science & Analytics',
                'class_standing': 'University Student',
                'cgpa': '3.52 / 4.00',
                'deans_list': True,
                'deans_list_detail': 'Consecutive semesters',
            },
        )

        EducationEntry.objects.update_or_create(
            institution='American University of Nigeria',
            defaults={
                'location': 'Yola, Nigeria',
                'program': 'B.Sc. Data Science & Analytics',
                'period': '2025 – Present',
                'description': (
                    'Developing knowledge in data science, analytics, '
                    'programming, and computational problem-solving.'
                ),
                'order': 0,
            },
        )
        EducationEntry.objects.update_or_create(
            institution='New Horizons College',
            defaults={
                'location': 'Minna, Niger State',
                'program': 'Secondary Education',
                'period': '',
                'description': (
                    'Provided the foundation for my academic journey and '
                    'helped develop the curiosity and discipline I continue '
                    'to apply to my university studies.'
                ),
                'order': 1,
            },
        )

        Achievement.objects.update_or_create(
            title="Dean's List Award",
            defaults={'detail': 'Consecutive semesters', 'order': 0},
        )
        Achievement.objects.update_or_create(
            title='Completed various tech bootcamps',
            defaults={'detail': 'e.g. GMT Software', 'order': 1},
        )

        prog_lang, _ = SkillCategory.objects.update_or_create(name='Programming Languages', defaults={'order': 0})
        db_tools, _ = SkillCategory.objects.update_or_create(name='Databases & Tools', defaults={'order': 1})
        other, _ = SkillCategory.objects.update_or_create(name='Other Skills', defaults={'order': 2})

        Skill.objects.update_or_create(category=prog_lang, name='Python', defaults={'order': 0})
        Skill.objects.update_or_create(category=db_tools, name='VS Code', defaults={'order': 0})
        Skill.objects.update_or_create(category=db_tools, name='GitHub', defaults={'order': 1})
        for i, name in enumerate(['Communication', 'Teamwork', 'Problem Solving', 'Public Speaking', 'Leadership']):
            Skill.objects.update_or_create(category=other, name=name, defaults={'order': i})

        self.stdout.write(self.style.SUCCESS('Seeded confirmed portfolio content.'))
