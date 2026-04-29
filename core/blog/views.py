from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "mohammad"
        return context


class RedirectToMaktab(RedirectView):
    permanent = False
    url = "https://maktabkhoone.com"


class PostList(ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 2
    ordering = "-created_date"
    # queryset = Post.objects.all()

    # def get_queryset(self):
    #     return super().get_queryset(self)


class PostListApiView(TemplateView):
    template_name = 'blog/post_list_api.html'


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    context_object_name = "post"
