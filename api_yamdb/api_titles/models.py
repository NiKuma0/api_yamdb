from datetime import datetime
from django.db import models
from django.core.validators import MaxValueValidator


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, primary_key=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug[:20]


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, primary_key=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug[:20]


class Titles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(
                datetime.now().year,
                message='Нельзя заглянуть в будущие!'
            ),
        ),
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Categories, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genres, related_name='titles')
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name[:20]

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведении'
