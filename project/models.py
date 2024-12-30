from django.db import models
from .constants import FRAMEWORKS
# Create your models here.

class Project(models.Model):

    github_url = models.URLField(max_length=1000, unique=True)
    subdomain = models.CharField(max_length=50, unique=True)
    framework = models.CharField(max_length=100, default="reactjs", choices=FRAMEWORKS)
    install_command = models.CharField(max_length=100, null=True, blank=True)
    build_command = models.CharField(max_length=100, null=True, blank=True)
    serve_command = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.github_url}"