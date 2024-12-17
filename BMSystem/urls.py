# urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    AdminHome, BookAdd,
    BookList,
    BookDelete, BookUpdate,
    Record, user_login, admin_login, user_register, combined_login, admin_register, logout_view, UserHome,
    user_profile,borrow_book,return_book,book_detail
)

urlpatterns = [
    path('login/', combined_login, name='combined_login'),
    path('admin/register/',admin_register, name='admin_register'),
    path('admin/login/',admin_login,name='admin_login'),
    path('user/login/',user_login,name='user_login'),
    path('user/register/', user_register, name='user_register'),
    path('logout/', logout_view, name='logout'),
    path('admin/home/', AdminHome, name='admin_home'),
    path('admin/book_list/', BookList, name='book_list'),
    path('admin/book_details/<int:pk>/', book_detail, name='book_detail'),
    path('admin/book_add/', BookAdd, name='book_add'),
    path('admin/book_delete/',BookDelete,name='book_delete'),
    path('admin/book_update/<int:pk>',BookUpdate,name='book_update'),
    path('admin/borrow_record', Record, name='borrow_record'),
    path('user/home',UserHome, name='user_home'),
    path('user/profile/', user_profile, name='user_profile'),
    path('user/borrow_book/', borrow_book, name='borrow_book'),
    path('user/return_book/', return_book, name='return_book'),

]