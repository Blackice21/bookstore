from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from bookstore_app.models import Book

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    my_ebooks = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.user.username

def My_post_save_signal(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)

post_save.connect(My_post_save_signal, sender=settings.AUTH_USER_MODEL)