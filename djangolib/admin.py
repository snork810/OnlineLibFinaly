from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(EBooksModel)
admin.site.register(Author)

class EBooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'summary', 'pages', 'category']
    search_fields = ['title', 'author', 'category']
