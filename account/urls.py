from django.urls import path
from . import api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", api.UserRegisterView.as_view()),
    path("email-verify/", api.VerifyEmail.as_view(), name="email-verify"),
    path("login/", TokenObtainPairView.as_view()),  # Login, Create a jwt token
    path("token/refresh/", TokenRefreshView.as_view()),  # Refresh an expired token
    path("auth/", api.AuthenticatedUserView.as_view()),  # Authenticated User
    path(
        "user/<int:pk>/",
        api.UserDetail.as_view(),
    ),  # CRUD operations on User
]
