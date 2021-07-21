from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import models
from django.core.validators import MaxValueValidator


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("name",)


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        ordering = ("name",)


class Titles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(datetime.now().year)],
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
