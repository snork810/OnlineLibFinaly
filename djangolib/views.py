from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from books.models import NoModeratedBooksModel


def home(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'djangolib/home.html', context)


def books_by_authors(request, pk):
    author = Author.objects.get(pk=pk)
    books = EBooksModel.objects.filter(author=pk)
    for book in books:
        book.available_formats = []
        if book.fb2:
            book.available_formats.append('fb2')
        if book.txt:
            book.available_formats.append('txt')
        if book.epub:
            book.available_formats.append('epub')

    user_favourite_ids = FavouriteBook.objects.filter(user=request.user).values_list('book_id',
                                                                                     flat=True)  # Получаем только ID
    context = {
        'books': books,
        'user_favourite_ids': user_favourite_ids,
        'author': author
    }
    return render(request, 'djangolib/books_by.html', context)


def search_books(request):
    book_title = request.GET.get('book_title')
    all_books = EBooksModel.objects.all()
    if book_title:
        books = all_books.filter(title__icontains=book_title)

    for book in books:
        book.available_formats = []
        if book.fb2:
            book.available_formats.append('fb2')
        if book.txt:
            book.available_formats.append('txt')
        if book.epub:
            book.available_formats.append('epub')

    user_favourite_ids = FavouriteBook.objects.filter(user=request.user).values_list('book_id',
                                                                                     flat=True)  # Получаем только ID
    context = {
        'books': books,
        'user_favourite_ids': user_favourite_ids,

    }
    return render(request, 'djangolib/search_book_results.html', context)


def search_authors(request):
    author_name = request.GET.get('author_name')
    all_authors = Author.objects.all()
    if author_name:
        author = all_authors.filter(name__icontains=author_name)
    context = {
        'author': author
    }
    return render(request, 'djangolib/search_author_result.html', context)


def library(request):
    books = EBooksModel.objects.order_by('author')
    for book in books:
        book.available_formats = []
        if book.fb2:
            book.available_formats.append('fb2')
        if book.txt:
            book.available_formats.append('txt')
        if book.epub:
            book.available_formats.append('epub')

    user_favourite_ids = FavouriteBook.objects.filter(user=request.user).values_list('book_id',
                                                                                     flat=True)  # Получаем только ID
    context = {
        'books': books,
        'user_favourite_ids': user_favourite_ids,  # Передаем IDs в контекст
    }
    return render(request, 'djangolib/library.html', context)


def approve_books(request):
    books_NMB = NoModeratedBooksModel.objects.all()

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = NoModeratedBooksModel.objects.get(pk=book_id)
        if not Author.objects.filter(name=book.author).exists():
            Author.objects.get_or_create(name=book.author, bio=f'Добавлен пользователем {request.user.username}')
            author_ex = Author.objects.get(name=book.author)
            approved_book = EBooksModel.objects.create(
                title=book.title,
                summary=book.summary,
                pages=book.pages,
                fb2=book.fb2,
                author=author_ex,
                cover_image=book.cover_image,
                category=book.category
            )
            favorite_book = FavouriteBook(user=request.user, book=approved_book)
            favorite_book.save()
            book.delete()
        else:
            author_ex = Author.objects.get(name=book.author)
            if not EBooksModel.objects.filter(title=book.title).exists():
                approved_book = EBooksModel.objects.create(
                    title=book.title,
                    summary=book.summary,
                    pages=book.pages,
                    fb2=book.fb2,
                    author=author_ex,
                    cover_image=book.cover_image,
                    category=book.category
                )
                favorite_book = FavouriteBook(user=request.user, book=approved_book)
                favorite_book.save()
                book.delete()
            else:
                approved_book = EBooksModel.objects.get(title=book.title)
                if not FavouriteBook.objects.filter(book=approved_book).exists():
                    favorite_book = FavouriteBook(user=request.user, book=approved_book)
                    favorite_book.save()
                    book.delete()
                else:
                    book.delete()

        return redirect('approve_books')

    context = {
        'books_NMB': books_NMB
    }
    return render(request, 'djangolib/approve_books.html', context)


def download_file(request, book_id):
    book = get_object_or_404(EBooksModel, id=book_id)

    selected_format = request.POST.get('format', 'txt')

    if selected_format == 'epub':
        file_path = book.epub.path
        content_type = 'application/octet-stream'
        file_name = f"{book.title}.epub"
    elif selected_format == 'fb2':
        file_path = book.fb2.path
        content_type = 'application/octet-stream'
        file_name = f"{book.title}.fb2"
    else:
        file_path = book.txt.path
        content_type = 'application/octet-stream'
        file_name = f"{book.title}.txt"

    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


def file_detail_lib(request, pk):
    file_instance = get_object_or_404(EBooksModel, pk=pk)
    RecentlyOpened.objects.get_or_create(user=request.user, book=file_instance)
    file_path = file_instance.fb2.path
    content_type = 'application/x-fictionbook+xml'
    file_name = f"{file_instance.title}.fb2"
    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{file_name}"'  # 'inline' разрешает открытие в браузере
    return response


@login_required
def add_to_favorites(request, book_id):
    book = EBooksModel.objects.get(id=book_id)
    if request.method == 'POST':
        favorite_book = FavouriteBook(user=request.user, book=book)
        favorite_book.save()
        return redirect('bookshelf')

    return render(request, 'djangolib/library.html', {'book': book})
