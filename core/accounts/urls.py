from django.urls import path, include
from . import views

urlpatterns = [
    path('send-email/', views.send_email, name="send_email"),
    path('test/', views.test, name='test'),
    path("api/v1/", include("accounts.api.v1.urls"), name="accounts_api"),
]
