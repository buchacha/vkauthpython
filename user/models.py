from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    vk_token = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)