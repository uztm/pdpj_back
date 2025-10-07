from django.db import models
from django.contrib.auth.models import User


class Month(models.Model):
    """Represents a calendar or academic month (e.g., January 2025, March 2025)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Month"
        verbose_name_plural = "Months"

    def __str__(self):
        return self.name


class Direction(models.Model):
    """Represents a study or teaching direction (e.g., Frontend, Backend, Design)."""
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Direction"
        verbose_name_plural = "Directions"

    def __str__(self):
        return self.title


class Mentor(models.Model):
    """Represents a teacher/mentor for a given direction."""
    full_name = models.CharField(max_length=150)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, related_name='mentors')
    image = models.ImageField(upload_to='mentors/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"

    def __str__(self):
        return self.full_name


class News(models.Model):
    """Represents a news article or announcement."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


class MonthHero(models.Model):
    """
    Represents a 'Hero of the Month' — either a student or a teacher
    recognized for achievements in a specific month.
    """
    HERO_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='heroes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='month_heroes')
    type = models.CharField(max_length=20, choices=HERO_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Month Hero"
        verbose_name_plural = "Month Heroes"
        unique_together = ('month', 'user', 'type')

    def __str__(self):
        return f"{self.get_type_display()} - {self.user.username} ({self.month.name})"
