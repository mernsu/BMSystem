# views.py
from datetime import date
from django.core.paginator import Paginator
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.messages.api import MessageFailure
from .forms import BookForm,BookUpdateForm,CustomAuthForm
from .models import Book
from django.shortcuts import render, redirect, get_object_or_404


def UserLogin(request):
    if request.method == 'POST':
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in successfully.")
                return redirect('home')  # 重定向到首页或其他页面
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = CustomAuthForm()
    return render(request, 'BMSystem/login.html', {'form': form})




def Home(request):
    books = Book.objects.all()
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'BMSystem/home.html', {'books': page_obj})

def BookList(request):
    books = Book.objects.all()
    return render(request, 'BMSystem/book_list.html', {'books': books})

def BookAdd(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        else:
            form = BookForm()
    return render(request, 'BMSystem/book_add.html', {'form': BookForm})

def BookDelete (request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        if isbn:
            # 尝试找到对应的书籍并删除
            books = Book.objects.filter(isbn=isbn)
            if books.exists():
                books.delete()
                messages.success(request, "ISBN为{}的书籍已经出库成功！".format(isbn))
            else:
                messages.error(request, "找不到ISBN为{}的书籍！".format(isbn))
        return redirect('book_delete')
    else:
        # 如果不是POST请求，显示删除页面
        return render(request, 'BMSystem/book_delete.html')

def BookUpdate(request):
    if request.method == 'POST':
        form = BookUpdateForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            messages.success(request, "The book has been updated successfully.")
            return redirect('book_list')  # 重定向到图书列表页面
    else:
        books = Book.objects.all()
        form = BookUpdateForm(initial={'isbn': '', 'title': '', 'author': '', 'publisher': '', 'published_date': '', 'stock': ''})
        for book in books:
            form.fields['isbn'].initial = book.isbn
            form.fields['title'].initial = book.title
            form.fields['author'].initial = book.author
            form.fields['publisher'].initial = book.publisher
            form.fields['published_date'].initial = book.published_date
            form.fields['stock'].initial = book.stock
    return render(request, 'BMSystem/book_update.html', {'form': form})







#未完成

class BookSearchView(ListView):
    model = Book
    template_name = 'BMSystem/book_list.html'



class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'published_date', 'stock']
    template_name = 'books/book_form.html'

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'published_date', 'stock']
    template_name = 'books/book_form.html'

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = '/book/'


class UserLoginView(LoginView):
    template_name = 'books/login.html'

class UserLogoutView(LogoutView):
    template_name = 'books/logout.html'

class BorrowBookView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = self.request.POST.get('book_id')
        book = Book.objects.get(id=book_id)
        record = BorrowRecord(book=book, My_user=self.request.user)
        record.save()
        return redirect('book_list')

class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = self.request.POST.get('book_id')
        record = BorrowRecord.objects.get(book_id=book_id, My_user=self.request.user, return_date__isnull=True)
        record.return_date = date.today()
        record.save()
        return redirect('book_list')