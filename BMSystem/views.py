# views.py
from django.contrib.auth.views import login_required
from django.contrib import messages
from .forms import BookForm,BookUpdateForm,AdminLoginForm
from .models import Book,BorrowRecord
from django.shortcuts import render, redirect,get_object_or_404
from datetime import date, timedelta
from .forms import CustomUserRegistrationForm,UserLoginForm,BorrowBookForm,ReturnBookForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse


def combined_login(request):
    return render(request, 'BMSystem/combined_login.html')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')  # 重定向到登录页面
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'BMSystem/user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_home')  # 重定向到用户首页
            else:
                form.add_error(None, '用户名或密码错误')
    else:
        form = UserLoginForm()
    return render(request, 'BMSystem/user_login.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            # 将 is_admin 设置为 True
            form.instance.is_admin = True
            form.save()
            return redirect('admin_login')  # 重定向到管理员登录页面
    else:
        form = CustomUserRegistrationForm(initial={'is_admin': True})
    return render(request, 'BMSystem/admin_register.html', {'form': form})
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.profile.is_admin:
                login(request, user)
                return redirect('admin_home')  # 重定向到管理员首页
            else:
                form.add_error(None, '无效的管理员凭证')
    else:
        form = AdminLoginForm()
    return render(request, 'BMSystem/admin_login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('combined_login')

#图书借阅端<!---------------------------------------------------------------------------------------------------------

def UserHome(request):
    # 获取每本书的借阅次数
    popular_books = Book.objects.annotate(num_bookings=Count('borrow_records')).order_by('-num_bookings')[:5]

    # 获取当前用户的借阅记录
    borrow_records = BorrowRecord.objects.filter(user=request.user)

    context = {
        'popular_books': popular_books,
        'borrow_records': borrow_records,
    }
    return render(request, 'BMSystem/user_home.html', context)


@login_required(login_url='user_login')
def user_profile(request):
    # 确保用户有关联的 Profile 模型实例
    profile = request.user.profile
    return render(request, 'BMSystem/user_profile.html', {'profile': profile})

@login_required
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']
            borrow_date = form.cleaned_data.get('borrow_date', date.today())
            return_date = form.cleaned_data.get('return_date')
            user = request.user

            book = Book.objects.filter(isbn=isbn).first()
            if book and book.stock > 0:
                BorrowRecord.objects.create(
                    book=book,
                    user=request.user,
                    borrow_date=borrow_date,
                    return_date=return_date
                )
                book.stock -= 1
                book.save()
                return render(request, 'BMSystem/borrow_book.html', {'form': form, 'success': True})
            else:
                form.add_error('isbn', '书籍不存在或已全部借出')
    else:
        form = BorrowBookForm()

    return render(request, 'BMSystem/borrow_book.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Book, BorrowRecord
from django.utils import timezone
from django.contrib.auth.decorators import login_required



@login_required
def return_book(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        book = get_object_or_404(Book, isbn=isbn)
        borrow_record = BorrowRecord.objects.filter(book=book, user=request.user, return_date__isnull=True).first()
        if borrow_record:
            # 执行归还逻辑
            borrow_record.return_date = timezone.now().date()
            borrow_record.save()
            book.stock += 1
            book.save()
            return JsonResponse({'message': 'Book returned successfully!'})
        else:
            return JsonResponse({'error': 'This book was not borrowed or has already been returned.'}, status=400)
    else:
        # 如果不是 POST 请求，显示归还表单
        return render(request, 'BMSystem/return_book.html')

#------------------------------------------------------------------------------------------------------------------!>




#图书管理端<!--------------------------------------------------------------------------------------------------------

@login_required(login_url='admin_login')
def AdminHome(request):
    popular_books = Book.objects.annotate(num_bookings=Count('borrow_records')).order_by('-num_bookings')[:5]

    # 每个月的借阅数据
    current_year = timezone.now().year
    current_month = timezone.now().month
    bookings_this_month = BorrowRecord.objects.filter(borrow_date__year=current_year, borrow_date__month=current_month).values('borrow_date__month').annotate(total=Count('id')).order_by('borrow_date__month')

    # 准备柱状图数据
    bar_chart_data = []
    for month in range(1, 13):
        month_bookings = bookings_this_month.filter(borrow_date__month=month).first()
        if month_bookings:
            bar_chart_data.append({
                'month': month,
                'total': month_bookings['total']
            })
        else:
            bar_chart_data.append({
                'month': month,
                'total': 0
            })

    context = {
        'popular_books': popular_books,
        'bar_chart_data': bar_chart_data,
    }
    return render(request, 'BMSystem/admin_home.html', context)

@login_required(login_url='admin_login')
def BookList(request):
    books = Book.objects.all()  # 获取所有书籍
    return render(request, 'BMSystem/book_list.html', {'book_list': books})

@login_required(login_url='admin_login')
def BookAdd(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        else:
            form = BookForm()
    return render(request, 'BMSystem/book_add.html', {'form': BookForm})

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
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

@login_required(login_url='admin_login')
def Record(request):
    # 获取所有的借阅记录
    records = BorrowRecord.objects.select_related('book', 'user').all()

    # 将借阅记录传递到模板
    return render(request, 'BMSystem/borrow_record.html', {'borrow_record': records})

#图书管理端--------------------------------------------------------------------------------------------------------!>








