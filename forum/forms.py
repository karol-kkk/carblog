from .models import Posts, Comment, PostImage
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django import forms
from django.forms import modelformset_factory
from django.forms import inlineformset_factory


class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'excerpt', 'body', 'published_at']

        # Blok widgets zajmuje się definicją pól w HTML. Tutaj można definiować typy wyświetlanych pół oraz zarządzać ich atrybutami.
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'excerpt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Excerpt'}),
            'body': Textarea(attrs={'class': 'form-control', 'placeholder': 'Post body'}),
            'published_at': DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Publication date'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    
    body = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2,  # This controls the height of the textarea (number of lines)
        'cols': 40  # This controls the width of the textarea (number of characters)
    }))


PostImageFormSet = inlineformset_factory(Posts, PostImage, fields=['image', 'description'], extra=1, can_delete=True)