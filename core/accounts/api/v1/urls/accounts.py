from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .. import views

urlpatterns = [
    # Registration
    path("register/", views.RegistrationApiView.as_view(), name="register"),
    path("test-email/", views.TestSendEmail.as_view(), name="test-email"),
    # Activation
    path(
        "activation/confirm/<str:token>/",
        views.ActivationApiView.as_view(),
        name="activation-confirm",
    ),
    # Resend Activation
    path(
        "activation/resend/",
        views.ResendActivationApiView.as_view(),
        name="activation-resend",
    ),
    # Change password
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # Re-Set password
    # Login Token
    path(
        "token/login/",
        views.CustomObtainAuthToken.as_view(),
        name="token-login",
    ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    # Login JWT
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
