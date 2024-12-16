# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    identity_card = models.CharField(max_length=18)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Book(models.Model):
    title = models.CharField(max_length=200)  # 书名
    author = models.CharField(max_length=100)  # 作者
    publisher = models.CharField(max_length=100)  # 出版社
    published_date = models.DateField(default=timezone.now)  # 出版年月
    stock = models.IntegerField(default=0)  # 库存数量
    isbn = models.CharField(max_length=13, unique=True, null=False, blank=False, default='')  # ISBN
    borrow_count = models.IntegerField(default=0)
    def __str__(self):
        return self.title



class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_records')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

