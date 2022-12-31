from django.urls import path
from . import api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", api_views.UserRegisterView.as_view()),
    path("email-verify/", api_views.VerifyEmail.as_view(), name="email-verify"),
    path("login/", TokenObtainPairView.as_view()),  # Login, Create a jwt token
    path("token/refresh/", TokenRefreshView.as_view()),  # Refresh an expired token
    path("auth/", api_views.AuthenticatedUserView.as_view()),  # Authenticated User
    path(
        "user/<int:pk>/",
        api_views.UserDetail.as_view(),
    ),  # CRUD operations on User
]
