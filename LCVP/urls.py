"""LCVP URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/lcvp/", include("account.urls")),
    path("api/v1/lcvp/", include("core.urls")),
]
