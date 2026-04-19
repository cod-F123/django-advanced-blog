from rest_framework import serializers
from rest_framework.request import Request
from accounts.models import Profile
from ...models import Post, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(
        source="get_absolute_api_url", read_only=True
    )
    absolute_url = serializers.SerializerMethodField(
        read_only=True, method_name="get_absolute_url"
    )

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        absolute_url = request.build_absolute_uri(obj.get_absolute_api_url())
        return absolute_url

    def to_representation(self, instance):

        rep = super().to_representation(instance)
        rep["category"] = CategorySerializer(instance.category).data

        request: Request = self.context.get("request")

        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet")
            rep.pop("relative_url")
            rep.pop("absolute_url")

        else:
            rep.pop("content")

        return rep

    def create(self, validated_data):
        request = self.context.get("request")

        validated_data["author"] = Profile.objects.get(
            user__id=request.user.id
        )

        return super().create(validated_data)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "snippet",
            "image",
            "content",
            "category",
            "relative_url",
            "absolute_url",
            "published_date",
            "created_date",
        ]
        read_only_fields = ["author"]
