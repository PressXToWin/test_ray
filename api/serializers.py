from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post
