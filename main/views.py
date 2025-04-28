# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce

from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from news.models import Articles

# Create your views here.
def index(request):
    recent_articles = Articles.objects.all().order_by('-published_at')[:3]
    return render(request, 'main/index.html', {'recent_articles': recent_articles})


def events(request):
    return render(request, 'main/events.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def sign_up (request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form":form})