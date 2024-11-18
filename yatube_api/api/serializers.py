from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import (Comment,
                          Post,
                          Group,
                          Follow,
                          User)
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True)
    image = serializers.CharField(required=False)
    group = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Group.objects.all())

    class Meta:
        fields = ('id', 'author', 'text',
                  'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author',
                  'text', 'created', 'post')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, required=False)
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow
