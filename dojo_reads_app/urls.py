# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('helper', views.helper),
    path('', views.face_page),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.main),
    path('books/add', views.add_book),
    path('books/create_book', views.create_book),
    path('books/<int:book_id>', views.show_book),
    path('books/reviews/<int:review_id>/delete', views.delete_review),
    path('users/<int:user_id>', views.user_page),
    

]
