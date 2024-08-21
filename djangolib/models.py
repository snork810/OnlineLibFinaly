
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class EBooksModel(models.Model):
    title = models.CharField('Название', max_length=80)
    summary = models.TextField('Аннотация',max_length=10000)
    pages = models.CharField("Количество страниц",max_length=80)
    txt = models.FileField("Загрузите файл в формате txt",upload_to='texts/txt/', null=True, blank=True)
    fb2 = models.FileField("Загрузите файл в формате fb2", upload_to='texts/fb2/', null=True, blank=True)
    epub = models.FileField("Загрузите файл в формате epub", upload_to='texts/epub/', null=True, blank=True)
    cover_image = models.ImageField("Обложка книги", upload_to='texts/covers/', null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.CharField("Категория",max_length=80)



    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Электронная книга'
        verbose_name_plural = 'Электронные книги'

class FavouriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(EBooksModel, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')


class RecentlyOpened(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(EBooksModel, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-opened_at']