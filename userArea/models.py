from django.db import models
from django import utils
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Games(models.Model):
    numbers = models.CharField('Numbers', max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)