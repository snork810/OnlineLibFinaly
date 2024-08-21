from django.db import models

# Create your models here.

class NoModeratedBooksModel(models.Model):
    title = models.CharField('Название', max_length=80)
    summary = models.TextField('Аннотация',max_length=10000)
    pages = models.IntegerField("Количество страниц")
    fb2 = models.FileField("Загрузите файл",upload_to='texts/nomoderated/')
    cover_image = models.ImageField("Обложка книги", upload_to='texts/nomoderated/covers/', null=True, blank=True)
    author = models.CharField('Автор', max_length=50)
    category = models.CharField("Категория",max_length=80)
    user = models.CharField('Введите свой никнэйм', max_length=80)



    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Не модерированное'