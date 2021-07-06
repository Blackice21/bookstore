from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import ManagerDescriptor

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    cover = models.ImageField()
    body = models.TextField()
    content = models.FileField(blank=True)
    genre = models.CharField(max_length=200, default='generic')
    price = models.FloatField(default=2.99)