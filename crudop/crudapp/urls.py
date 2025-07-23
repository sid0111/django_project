from django.urls import path
from .import views

urlpatterns = [
   path('',views.book_list, name='book_list'),
   path('create/', views.book_create, name='book_create'),
   path('books/<int:id>/edit/', views.book_update, name='book_update'),
    path('books/<int:id>/delete/', views.book_delete, name='book_delete'),

  
]

