from .models import NoModeratedBooksModel
from django.forms import ModelForm, TextInput, NumberInput, FileInput, Textarea


class NoModeratedBooksModelForm(ModelForm):
    class Meta:
        model = NoModeratedBooksModel
        fields = ['title', 'summary', 'pages', 'fb2', 'author', 'category', 'user', 'cover_image']
        widgets = {
            'title': TextInput(attrs={
                    'class': "form-control",
                    'placeholder': "Название книги"
            }),
            'summary': Textarea(attrs={
                'class': "form-control",
                'placeholder': "Аннотация"
            }),
            'author': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Автор"
            }),
            'category': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Жанр"
            }),
            'pages': NumberInput(attrs={
                'class': "form-control",
                'placeholder': "Количество страниц"
            }),
            'fb2': FileInput(attrs={
                'class': "form-control",
                'placeholder': "Загрузите фаш файл в формате FB2"
            }),
            'cover_image':FileInput(attrs={
                'class': "form-control",
                'placeholder': "Загрузите обложку вашей книги"
            }),
            'user':TextInput(attrs={
                'class': "form-control",
                'placeholder': "Ваш никнейм"
            })
        }