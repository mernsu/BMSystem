from django import forms
from .models import Book
from django.contrib.auth.forms import AuthenticationForm

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

class CustomAuthForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Remember me")

    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    def clean(self):
        cleaned_data = super(CustomAuthForm, self).clean()
        remember_me = cleaned_data.get('remember_me')
        if remember_me:
            # 设置记住我的逻辑，例如设置一个长时间的session
            pass
        return cleaned_data
    pass



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

