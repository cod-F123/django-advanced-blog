from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your models here.


class Post(models.Model):
    """
    This class defines the post model
    """

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts/%Y/%m", blank=True, null=True)
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True
    )
    status = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.content[0:10]

    def get_absolute_api_url(self):
        return reverse("blog:api_v1:post-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    """
    This class defines the category model for posts
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
