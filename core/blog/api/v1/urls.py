from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "api_v1"


router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")

urlpatterns = router.urls

# urlpatterns = [
#     # path('post/', views.api_post_list_view, name='post-list'),
#     # path('post/', views.PostListApiView.as_view(), name= 'post-list'),
#     # path('post/<int:pk>/', views.api_post_detail_view, name='post-detail'),
#     # path('post/<int:pk>/', views.PostDetailApiView.as_view(), name='post-detail'),
#
#     path('post/', views.PostViewSet.as_view({'get':"list", 'post':"create"}), name='post'),
#     path('post/<int:pk>/', views.PostViewSet.as_view({'get':"retrieve", 'put':"update", 'patch':"partial_update", 'delete':"destroy"}), name='detail'),
# ]
