from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bookshelf, name='bookshelf'),
    path('addbook/', views.addbook, name='addbook'),
    path('files_FB/<int:pk>/', views.file_detail_FB, name='file_detail_FB'),
    path('file_NMB/<int:pk>/', views.file_detail_NMB, name='file_detail_NMB'),
    path('file_RO/<int:pk>/', views.file_detail_RO, name='file_detail_RO'),
    path('delete/<int:pk>/', views.delete_no_moderated_book, name='delete_no_moderated_book'),

]