from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import NoModeratedBooksModel
from .forms import NoModeratedBooksModelForm

from django.contrib.auth.decorators import login_required

from djangolib.models import FavouriteBook, RecentlyOpened

@login_required
def bookshelf(request):
    files = NoModeratedBooksModel.objects.filter(user=request.user.username)
    favorites = FavouriteBook.objects.filter(user=request.user)
    recently_opened_books = RecentlyOpened.objects.filter(user=request.user).select_related('book')[:5]
    context = {
        'files': files,
        'favorites': favorites,
        "recently_opened_books": recently_opened_books
    }
    return render(request, 'books/bookshelf.html', context)


def addbook(request):
    error = ''
    if request.method == "POST":
        form = NoModeratedBooksModelForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Привязка книги к пользователю
            book.save()
            return redirect('bookshelf')
        else:
            error = 'Форма была заполнена некорректно'

    form = NoModeratedBooksModelForm()
    context = {'form': form,
               'error': error
               }
    return render(request, 'books/addbook.html', context)

def file_detail_FB(request,  pk):
    file_instance = get_object_or_404(FavouriteBook, pk=pk)

    # Получаем путь к FB2-формату книги
    file_path = file_instance.book.fb2.path
    content_type = 'application/x-fictionbook+xml'
    file_name = f"{file_instance.book.title}.fb2"

    # Возвращаем ответ для открытия файла в браузере
    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{file_name}"'  # 'inline' разрешает открытие в браузере
    return response
def file_detail_RO(request,  pk):
    file_instance = get_object_or_404(RecentlyOpened, pk=pk)

    # Получаем путь к FB2-формату книги
    file_path = file_instance.book.fb2.path
    content_type = 'application/x-fictionbook+xml'
    file_name = f"{file_instance.book.title}.fb2"

    # Возвращаем ответ для открытия файла в браузере
    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{file_name}"'  # 'inline' разрешает открытие в браузере
    return response
def file_detail_NMB(request,  pk):
    file_instance = get_object_or_404(NoModeratedBooksModel, pk=pk)

    # Получаем путь к FB2-формату книги
    file_path = file_instance.fb2.path
    content_type = 'application/x-fictionbook+xml'
    file_name = f"{file_instance.title}.fb2"

    # Возвращаем ответ для открытия файла в браузере
    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{file_name}"'  # 'inline' разрешает открытие в браузере
    return response

@login_required
def delete_no_moderated_book(request, pk):
    book = get_object_or_404(NoModeratedBooksModel, pk=pk, user=request.user.username)  # Проверяем, что книга принадлежит пользователю

    if request.method == 'POST':
        book.fb2.delete(save=False)  # Удалить файл из файловой системы
        book.delete()  # Удалить запись из базы данных
        return redirect('bookshelf')  # Перенаправить на страницу личного кабинета

    return render(request, 'books/confirm_delete.html', {'book': book})