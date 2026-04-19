from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets

from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from .permissions import IsOwnerOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .paginations import DefaultPagination

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticatedOrReadOnly,])
# def api_post_list_view(request):
#
#     if request.method == 'GET':
#
#         posts = Post.objects.all()
#
#         serializer = PostSerializer(posts, many=True)
#
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data)


# class PostListApiView(APIView):
#     """ get a list of posts and create a new post """
#
#     permission_classes = [IsAuthenticatedOrReadOnly,]
#     serializer_class = PostSerializer
#
#     def get(self, request):
#         """ retrieve a list of posts """
#
#         posts = Post.objects.all()
#
#         serializer = PostSerializer(posts, many=True)
#
#         return Response(serializer.data)
#
#     def post(self, request):
#         """ create a new post"""
#
#         serializer = PostSerializer(data=request.data)
#
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data)


# class PostListApiView(GenericAPIView, mixins.ListModelMixin ,mixins.CreateModelMixin):
#     """ get a list of posts and create a new post """
#
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#
#     def get(self, request, *args, **kwargs):
#
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class PostListApiView(ListCreateAPIView):
    """get a list of posts and create a new post"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# @api_view()
# def api_post_detail_view(request, pk):
#
#     post = get_object_or_404(Post, pk=pk)
#
#     serializer  = PostSerializer(post)
#
#     return Response(serializer.data)

# class PostDetailApiView(APIView):
#     """ get a post and update and delete a post"""
#
#     permission_classes = [IsAuthenticatedOrReadOnly,]
#     serializer_class = PostSerializer
#
#     def get(self, request, pk):
#         """ getting a post """
#
#         post = get_object_or_404(Post, pk=pk)
#
#         serializer = self.serializer_class(post)
#
#         return  Response(serializer.data)
#
#     def put(self, request, pk):
#         """ updating a post """
#
#         post = get_object_or_404(Post, pk=pk)
#
#         serializer = self.serializer_class(post, request.data)
#
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         """ deleting a post """
#
#         post = get_object_or_404(Post, pk=pk)
#
#         post.delete()
#
#         return Response({"detail": "post deleted successfully !."},status=status.HTTP_204_NO_CONTENT)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    lookup_field = "pk"


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]

    pagination_class = DefaultPagination

    @action(detail=False, methods=["get"])
    def get_ok(self, request):
        return Response({"detail": "ok"})


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    serializer_class = CategorySerializer
