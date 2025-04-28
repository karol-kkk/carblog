from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, DeleteView
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from .models import Articles, ArticleImage
from .forms import ArticlesForm, ArticleImageFormSet
from django.contrib.auth.decorators import login_required

# Create your views here.

def news_home(request):
    news = Articles.objects.all().order_by('-published_at')
    return render(request, 'news/index.html', {'news': news})

@login_required
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

class NewsUpdateView(UpdateView):
    model = Articles
    form_class = ArticlesForm
    template_name = 'news/update.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = get_object_or_404(Articles, pk=self.kwargs['pk'])
        return article

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.author != request.user:
            return HttpResponseForbidden("You are not allowed to access this article.")
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        article = form.save(commit=False)
        if article.author != self.request.user:
            return HttpResponseForbidden("You are not allowed to update this article.")
        
        formset = ArticleImageFormSet(self.request.POST, self.request.FILES, instance=article)
        if formset.is_valid():
            article.save() 
            formset.save() 
            return redirect('news_show', pk=article.pk)
        
        return self.render_to_response({'form': form, 'formset': formset})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['formset'] = ArticleImageFormSet(self.request.POST or None, self.request.FILES or None, instance=article)
        return context

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/delete.html'
    success_url = '/news/'

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.author != request.user:
            return HttpResponseForbidden("You are not allowed to delete this article.")
        return super().dispatch(request, *args, **kwargs)    