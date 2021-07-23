from django.db import models
from django.db.models.constraints import CheckConstraint, Q
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model

from api_titles.models import Titles


User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=(MaxValueValidator(10),)
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.score)[:4]

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = (
            CheckConstraint(
                check=Q(score__lte=10),
                name='score_constraint'),
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_constraint'),
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
