from .models import Articles, ArticleImage
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, ClearableFileInput
from django import forms
from django.forms import modelformset_factory
from django.forms import inlineformset_factory

class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'excerpt', 'body', 'thumbnail']

        # Blok widgets zajmuje się definicją pól w HTML. Tutaj można definiować typy wyświetlanych pół oraz zarządzać ich atrybutami.
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'excerpt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Excerpt'}),
            'body': Textarea(attrs={'class': 'form-control', 'placeholder': 'Article body'}),
            'published_at': DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Publication date'}),
            'thumbnail': ClearableFileInput(attrs={'class': 'form-control'}),
        }

ArticleImageFormSet = inlineformset_factory(Articles, ArticleImage, fields=['image', 'description'], extra=1, can_delete=True)