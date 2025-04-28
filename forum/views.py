from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .models import Posts, Comment, PostImage
from .forms import PostsForm, CommentForm, PostImageFormSet
from django.http import HttpResponseForbidden

# Create your views here.
def index(request):
    return render(request,'forum/index.html') 

def frequent_questions(request):
    return render(request,'forum/frequent_questions.html') 


def post_home(request):
    posts = Posts.objects.all().order_by('-published_at')
    return render(request, 'forum/index.html', {'posts': posts})

@login_required
def post_create(request):
    error = ''
    if request.method == 'POST':
        form = PostsForm(request.POST)
        formset = PostImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            for image_form in formset:

                if image_form.cleaned_data and not image_form.cleaned_data.get('DELETE', False):
                    image = image_form.save(commit=False)
                    image.post = new_post
                    image.save()

            return redirect(new_post.get_absolute_url())
        else:
            error = 'Submitted form contains errors.'
    else:
        form = PostsForm()
        formset = PostImageFormSet()

    data = {
        'form': form,
        'formset': formset,
        'error': error,
    }
    return render(request, 'forum/create.html', data)

class PostDetailView(DetailView):
    model = Posts
    template_name = 'forum/show.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() ### loads the current post, it's needed to associate the new comment with this post
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post_show', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

class PostUpdateView(UpdateView):
    model = Posts
    form_class = PostsForm
    template_name = 'forum/update.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(Posts, pk=self.kwargs['pk'])
        return post

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to access this post.")
        return super().dispatch(request, *args, **kwargs)  

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.author != self.request.user:
            return HttpResponseForbidden("You are not allowed to update this post.")
        
        formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=post)
        if formset.is_valid():
            post.save() 
            formset.save() 
            return redirect('post_show', pk=post.pk)
        
        return self.render_to_response({'form': form, 'formset': formset})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['formset'] = PostImageFormSet(self.request.POST or None, self.request.FILES or None, instance=post)
        return context

class PostDeleteView(DeleteView):
    model = Posts
    template_name = 'forum/delete.html'
    success_url = '/forum/'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to delete this post.")
        return super().dispatch(request, *args, **kwargs)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author: 
                comment.delete()

    return redirect('post_show', pk=comment.post.pk)