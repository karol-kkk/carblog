from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Articles(models.Model):
    title = models.CharField('Article title', max_length=100, null=False, blank=False)
    excerpt = models.CharField('Article excerpt', max_length=250, null=False, blank=False)
    body = models.TextField('Article body', null=False, blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='article_images/', blank=False, null=True)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

class ArticleImage(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for Article {self.article.id}"