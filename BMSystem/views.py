# views.py
from django.contrib.auth.views import login_required
from django.contrib import messages
from .forms import BookForm, BookUpdateForm, AdminLoginForm
from .models import Book, BorrowRecord
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
from .forms import CustomUserRegistrationForm, UserLoginForm, BorrowBookForm, ReturnBookForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.utils import timezone
<<<<<<< HEAD
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from functools import wraps


=======
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from functools import wraps






>>>>>>> 8ccf56837753743090847d0bf0f4c015ed923be0
def admin_required(view_func):
    @wraps(view_func)
    @login_required  # 确保用户已经登录
    def _wrapped_view(request, *args, **kwargs):
        # 检查用户是否有Profile实例，并且是否标记为管理员
        if request.user.is_authenticated and request.user.profile.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            # 如果不是管理员，返回403禁止访问
            return HttpResponseForbidden()
<<<<<<< HEAD

=======
>>>>>>> 8ccf56837753743090847d0bf0f4c015ed923be0
    return _wrapped_view


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
    popular_books = Book.objects.annotate(num_bookings=Count('borrow_count')).order_by('-num_bookings')[:5]

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


@login_required(login_url='user_login')
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn'].strip()  # 去除ISBN前后的空格
            try:
                book = Book.objects.get(isbn=isbn)
            except Book.DoesNotExist:
                return JsonResponse({'status': 'error', 'error': '借阅失败！ISBN为“' + isbn + '”的书籍不存在'},
                                    status=404)

            if book.stock > 0:
                due_date = form.cleaned_data.get('due_date', timezone.now().date())  # 如果未提供预计归还日期，则默认为当前日期
                borrow_record = BorrowRecord.objects.create(
                    book=book,
                    user=request.user,
                    borrow_date=timezone.now().date(),
                    due_date=due_date
                )
                book.stock -= 1
                book.save()
                return JsonResponse({'status': 'success', 'message': '借阅成功！'})
            else:
                return JsonResponse({'status': 'error', 'error': '借阅失败！该书已无库存。'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'error': '请输入有效的ISBN号。'}, status=400)
    else:
        form = BorrowBookForm()
        return render(request, 'BMSystem/borrow_book.html', {'form': form})


@login_required(login_url='user_login')
def return_book(request):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']

            try:
                book = Book.objects.get(isbn=isbn)
            except Book.DoesNotExist:
                # 如果书籍不存在，返回错误消息
                return JsonResponse({'status': 'error', 'error': '请输入有效的ISBN号。'}, status=400)

            borrow_record = BorrowRecord.objects.filter(book=book, user=request.user, return_date__isnull=True).first()

            if borrow_record:
                borrow_record.return_date = timezone.now().date()
                borrow_record.save()

                book.stock += 1
                book.save()

                return JsonResponse({'status': 'success', 'message': '图书已成功归还。'})
            else:
                return JsonResponse({'status': 'error', 'error': '您没有借阅这本书或已归还。'})
        else:
            # 表单验证失败，返回错误消息
            return JsonResponse({'status': 'error', 'error': '请输入有效的ISBN号。'}, status=400)
    else:
        form = ReturnBookForm()
        return render(request, 'BMSystem/return_book.html', {'form': form})


#------------------------------------------------------------------------------------------------------------------!>


#图书管理端<!--------------------------------------------------------------------------------------------------------


@admin_required
def AdminHome(request):
    popular_books = Book.objects.annotate(num_bookings=Count('borrow_count')).order_by('-num_bookings')[:5]

    # 每个月的借阅数据
    current_year = timezone.now().year
    current_month = timezone.now().month
    bookings_this_month = BorrowRecord.objects.filter(borrow_date__year=current_year,
                                                      borrow_date__month=current_month).values(
        'borrow_date__month').annotate(total=Count('id')).order_by('borrow_date__month')

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


@admin_required
def BookList(request):
    books = Book.objects.all()  # 获取所有书籍
    return render(request, 'BMSystem/book_list.html', {'books': books})


@admin_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'BMSystem/book_detail.html', {'book': book})


@admin_required
def BookAdd(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        else:
            form = BookForm()
    return render(request, 'BMSystem/book_add.html', {'form': BookForm})


@admin_required
<<<<<<< HEAD
def BookDelete(request):
=======
def BookDelete (request):
>>>>>>> 8ccf56837753743090847d0bf0f4c015ed923be0
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


<<<<<<< HEAD
=======

>>>>>>> 8ccf56837753743090847d0bf0f4c015ed923be0
@admin_required
def BookUpdate(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'BMSystem/book_update.html', {'form': form})


<<<<<<< HEAD
=======

>>>>>>> 8ccf56837753743090847d0bf0f4c015ed923be0
@admin_required
def Record(request):
    records = BorrowRecord.objects.select_related('book', 'user').all()
    return render(request, 'BMSystem/borrow_record.html', {'borrow_record': records})

#图书管理端--------------------------------------------------------------------------------------------------------!>
