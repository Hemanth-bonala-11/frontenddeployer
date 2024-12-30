from django.contrib import admin
from .models import Project

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('github_url', 'subdomain', 'framework')
    search_fields = ('github_url', 'subdomain')
    list_filter = ('created_at', 'updated_at')