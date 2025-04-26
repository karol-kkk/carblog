from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, DeleteView
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from .models import Articles, ArticleImage
from .forms import ArticlesForm, ArticleImageFormSet

# Create your views here.

def news_home(request):
    news = Articles.objects.all().order_by('-published_at')
    return render(request, 'news/index.html', {'news': news})

def news_create(request):
    error = ''

    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES)
        formset = ArticleImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            if not request.user.is_superuser:
                return HttpResponseForbidden("Only superusers can create news articles.")
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.save()

            for image_form in formset:

                if image_form.cleaned_data and not image_form.cleaned_data.get('DELETE', False):
                    image = image_form.save(commit=False)
                    image.article = new_article
                    image.save()

            return redirect(new_article.get_absolute_url())
        else:
            error = 'Submitted form contain errors'

    else:
        form = ArticlesForm()
        formset = ArticleImageFormSet()

    data = {
        'form': form,
        'formset': formset,
        'error': error,
    }
    return render(request, 'news/create.html', data)

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/show.html'
    context_object_name = 'article'

def update_article(request, pk):
    article = get_object_or_404(Articles, pk=pk)

    if article.author != request.user:
        return HttpResponseForbidden("You are not allowed to update this article.")

    article_form = ArticlesForm(request.POST or None, instance=article)
    formset = ArticleImageFormSet(request.POST or None, request.FILES or None, instance=article)

    if article_form.is_valid() and formset.is_valid():
        article_form.save()
        formset.save()
        return redirect('news_show', pk=article.pk)

    return render(request, 'news/update.html', {
        'article_form': article_form,
        'formset': formset,
    })


class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/delete.html'
    success_url = '/news/'

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.author != request.user:
            return HttpResponseForbidden("You are not allowed to delete this article.")
        return super().dispatch(request, *args, **kwargs)    