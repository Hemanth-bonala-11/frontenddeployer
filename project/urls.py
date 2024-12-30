from django.contrib import admin
from django.urls import path, re_path
from .views import RenderTemplateView, DeployView

urlpatterns = [
    path('api/deploy/', DeployView.as_view(), name="deploy-view"),
    re_path(r"^(?:.*)/?$", RenderTemplateView.as_view(), name="render-template-api"),
]
