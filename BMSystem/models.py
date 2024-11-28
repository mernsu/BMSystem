# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)  # 书名
    author = models.CharField(max_length=100)  # 作者
    publisher = models.CharField(max_length=100)  # 出版社
    published_date = models.DateField(default=timezone.now)  # 出版年月
    stock = models.IntegerField(default=0)  # 库存数量
    isbn = models.CharField(max_length=13, unique=True, null=False, blank=False, default='')  # ISBN
    def __str__(self):
        return self.title

