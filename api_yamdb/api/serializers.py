from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import (
    User, Title, Genre, Category, Review, Comments)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о пользователях."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'bio', 'role')


class UserSignSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Имя пользователя не может быть <me>.'
            )
        return value


class UserGetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получение токенов пользователей."""

    username = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        required=False
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', )


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        required=False
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date', )
