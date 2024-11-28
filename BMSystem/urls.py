# urls.py

from django.urls import path
from .views import (
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    UserLoginView,
    UserLogoutView,
    BorrowBookView,
    ReturnBookView,
    Home, BookSearchView, BookAdd,
    BookList,
    BookDelete, BookUpdate,
    UserLogin,
)

urlpatterns = [
    path('login/',UserLogin,name='user_login'),
    path('home/', Home, name='home'),
    path('book_list/', BookList, name='book_list'),
    path('book_search/', BookSearchView.as_view(), name='book_search'),
    path('book_add/', BookAdd, name='book_add'),
    path('book_delete/',BookDelete,name='book_delete'),
    path('book_update',BookUpdate,name='book_update'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/new/', BookCreateView.as_view(), name='book_new'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('return/', ReturnBookView.as_view(), name='return_book'),
]