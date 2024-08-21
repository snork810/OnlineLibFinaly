"""
URL configuration for DjangoLibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from djangolib import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('library/', views.library, name='library'),
    path('library/files/<int:pk>/', views.file_detail_lib, name='file_detail_lib'),
    path('favourite/<int:book_id>/', views.add_to_favorites, name='favourite'),
    path('download/<int:book_id>/', views.download_file, name='download_file'),
    path('books_by/<int:pk>', views.books_by_authors, name='books_by'),
    path('search_books/', views.search_books, name='search_books'),
    path('search_authors/', views.search_authors, name='search_authors'),
    path('approve_books/', views.approve_books, name='approve_books'),
    path('bookshelf/', include('books.urls')),
    path('accounts/', include('registration.urls', namespace="accounts")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)