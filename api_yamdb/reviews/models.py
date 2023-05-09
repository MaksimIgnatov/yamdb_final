from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import year_validate

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=250
    )
    slug = models.SlugField(
        verbose_name='URL',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='URL',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[year_validate],
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категории',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True,
                                    db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[15]
