from email.policy import default
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Book,Profile
from django.contrib.auth.forms import AuthenticationForm,User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
import datetime

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher','published_date','stock','isbn']
        labels = {
            'title': '书名',
            'author': '作者',
            'publisher': '出版社',
            'published_date': '出版日期',
            'stock':'数目',
            'isbn' : 'ISBN',
        }



class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'isbn', 'published_date', 'stock']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': '书名',
            'author': '作者',
            'publisher': '出版社',
            'published_date': '出版日期',
            'stock':'数目',
            'isbn' : 'ISBN',
        }



class BorrowBookForm(forms.Form):
    isbn = forms.CharField(label='ISBN号', max_length=13)
    due_date = forms.DateField(label='预计归还日期', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        isbn = cleaned_data.get('isbn')
        due_date = cleaned_data.get('due_date')

        if due_date and due_date <= timezone.now().date():
            raise forms.ValidationError("预计归还日期必须在当前日期之后。")

        return cleaned_data

class ReturnBookForm(forms.Form):
    isbn = forms.CharField(label='ISBN号', max_length=13)

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='用户名', max_length=64)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(label='用户名', max_length=64)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

class CustomUserRegistrationForm(UserCreationForm):
    name = forms.CharField(label='姓名', max_length=100)
    identity_card = forms.CharField(label='身份证号', max_length=18)
    is_admin = forms.BooleanField(label='是否为管理员', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'name', 'identity_card')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']  # 设置用户的 first_name
        if commit:
            user.save()
            # 创建 Profile 实例时包含 name 和 identity_card
            Profile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                identity_card=self.cleaned_data['identity_card'],
                is_admin=self.cleaned_data['is_admin']
            )
        return user