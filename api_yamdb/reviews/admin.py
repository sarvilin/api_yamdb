from django.contrib import admin

from .models import User, Category, Title, Genre, GenreTitle, Review, Comments

admin.site.register(User)

admin.site.register(Category)

admin.site.register(Title)

admin.site.register(Genre)

admin.site.register(GenreTitle)

admin.site.register(Review)

admin.site.register(Comments)
