from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    cover = models.ImageField()
    body = models.TextField()
    content = models.FileField()