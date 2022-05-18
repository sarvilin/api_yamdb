from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    ReviewViewSet, CommentsViewSet, UserViewSet,
                    APIGetToken, APISignup)

router = DefaultRouter()
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register(
    'users',
    UserViewSet,
    basename='users'
)
router.register(
    r'users/me',
    UserViewSet,
    basename="users_me"
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
]
