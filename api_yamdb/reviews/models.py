from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reviews.validators import validate_year

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """Модель для создания таблицы Пользователи."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель для создания таблицы Категории."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для создания таблицы Жанры."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для создания таблицы Произведения."""

    name = models.CharField(max_length=200)
    year = models.IntegerField(
        'год',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre')
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для создания связанной таблицы Жанры-Произведения."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )


class Review(models.Model):
    """Модель для создания таблицы Отзывы."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=1)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='review_unique')
        ]


class Comments(models.Model):
    """Модель для создания таблицы Комментарии."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
