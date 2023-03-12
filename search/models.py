from django.db import models
from django.contrib.auth.models import User

class FavoriteManga(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga_id = models.IntegerField()