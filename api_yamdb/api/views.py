import random
import string

from django.conf import settings
from django.core import mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, serializers, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Title, Category, Genre, Review
from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import (
    IsAdminUserOrReadOnly, AdminModeratorAuthorPermission, AdminOnly)
from .serializers import (
    UserSerializer, CategorySerializer, GenreSerializer, ReviewSerializer,
    CommentsSerializer, TitleReadSerializer, TitleWriteSerializer,
    UserGetTokenSerializer, UserSignSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
        url_name='me'
    )
    def me(self, request):
        user_me = self.request.user
        serializer = self.get_serializer(user_me)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user_me,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                email=user_me.email,
                role=user_me.role
            )
        return Response(serializer.data)


class CategoryViewSet(ModelMixinSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ModelMixinSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(rating=Avg(
        'review__score')).order_by('-id')
    serializer_class = TitleWriteSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для списка отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        new_queryset = title.review.all().order_by('-id')
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.request.user
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв.")
        serializer.save(title=title, author=author)


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для списка комментариев."""

    serializer_class = CommentsSerializer
    permission_classes = (AdminModeratorAuthorPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        new_queryset = review.comments.all().order_by('-id')
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)


class APIGetToken(APIView):
    """Вьюкласс для получения токенов."""

    serializer_class = UserGetTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        user_data = {'username', 'confirmation_code'}
        if user_data.issubset(serializer.initial_data.keys()):
            if get_object_or_404(User, username=serializer.initial_data.get(
                    'username')):
                if serializer.is_valid():
                    user = User.objects.filter(
                        username=serializer.validated_data.get('username'),
                        confirmation_code=serializer.validated_data.get(
                            'conformation_code'))
                    if user.exists():
                        refresh = RefreshToken.for_user(user)
                        return Response(
                            data={'token': str(refresh.access_token)},
                            status=status.HTTP_200_OK
                        )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """Вьюкласс для регистрации пользователей."""

    serializer_class = UserSignSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.sample(letters, 16))
        serializer = UserSignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['confirmation_code'] = rand_string
            serializer.save()
            mail.send_mail(
                settings.EMAIL_THEME,
                settings.EMAIL_TEXT,
                settings.EMAIL_HOST,
                [serializer.validated_data['email']],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
