from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "go-to-maktab", views.RedirectToMaktab.as_view(), name="go-to-maktab"
    ),
    path("list/", views.PostList.as_view(), name="list"),
    path('list/api/', views.PostListApiView.as_view(), name="list-api"),
    path("detail/<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("api/v1/", include("blog.api.v1.urls")),
]
