from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet, GroupViewSet,
                    CommentViewSet, FollowViewSet)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

router = DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet,
                basename='post-comments')
router.register('posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'follow', FollowViewSet)

urlpatterns = [
    path('v1/jwt/create/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/jwt/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/jwt/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),
    path('v1/', include(router.urls)),
]
