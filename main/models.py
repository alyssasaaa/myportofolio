import uuid

from django.db import models

# Create your models here.
class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
        ("committee", "Committee"),
        ("organization", "Organization"),
    ]

    STAGE_CHOICES = [
            ("university", "University"),
            ("high-school", "High School"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    stage = models.CharField(
            max_length=20,
            choices=STAGE_CHOICES,
            default="university",
        )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education (models.Model):
    institution = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    description = models.TextField()
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True)
    skills = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.institution

    @property
    def is_current(self):
        return self.end_year is None

    @property
    def skills_list(self):
        return [
            skill.strip()
            for skill in self.skills.split(",")
            if skill.strip()
        ]