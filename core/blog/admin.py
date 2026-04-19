from django.contrib import admin
from .models import Post, Category

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "status",
        "created_date",
        "published_date",
    )
    search_fields = ("author__email", "title")
    list_filter = ("status",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
