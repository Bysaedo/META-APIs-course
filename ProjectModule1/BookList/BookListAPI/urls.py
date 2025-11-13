from django.urls import path
from . import views


urlpatterns = [
  #path('books/', views.books),
  #path('books/',views.BookList.as_view()),
  #path('books/<int:pk>', views.SingleBook.as_view()),
  path('books/', views.BookView.as_view()),
  path('books/<int:pk>', views.BookDetailView.as_view(), name='SingleBook')
  ]