# TODO:  Напишите свой вариант
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import (ModelViewSet,
                                     ReadOnlyModelViewSet,
                                     GenericViewSet)
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from api.serializers import (PostSerializer, GroupSerializer,
                             CommentSerializer, FollowSerializer)
from posts.models import Post, Group, Comment, Follow
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)
    read_only_fields = ('author', 'pub_date',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().partial_update(request,
                                      *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request,
                              *args, **kwargs)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def list(self, request, post_id):
        try:
            queryset = Comment.objects.filter(post_id=post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self):
        queryset = self.queryset.filter(post=self.kwargs['post_id'])
        obj = queryset.get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, post_id):
        if request.method == "POST":
            user = request.user
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['author'] = user
                serializer.validated_data['post'] = (Post
                                                     .objects
                                                     .get(pk=post_id))
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def list(self, request, *args, **kwargs):
        data = self.filter_queryset(self.
                                    queryset.filter(user=request.user))
        serializer = FollowSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():

            serializer.validated_data['user'] = user
            if serializer.validated_data['following'] == user:
                raise ValidationError(code=400,
                                      detail={
                                          'detail':
                                              'You cannot follow yourself!'
                                      })
            try:
                Follow.objects.get(user=user,
                                   following=serializer
                                   .validated_data['following'])
            except Follow.DoesNotExist:
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
