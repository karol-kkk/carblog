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
    values = {
        'events': [
            {
                'event': 'Drift Masters Round 1',
                'country': 'Italy',
                'date': '25-26.04.2025',
                'track': 'Vallelunga Circuit',
            },
            {
                'event': 'Drift Masters Round 2',
                'country': 'Spain',
                'date': '17-18.05.2025',
                'track': 'Circuito de Madrid Jarama - RACE',
            },
            {
                'event': 'Drift Masters Round 3',
                'country': 'Finland',
                'date': '06-07.06.2025',
                'track': 'Power Park Huvivaltio',
            },
            {
                'event': 'Drift Masters Round 4',
                'country': 'Ireland',
                'date': '28-29.06.2025',
                'track': 'Mondello Park',
            },
            {
                'event': 'Drift Masters Round 5',
                'country': 'Latvia',
                'date': '25-26.07.2025',
                'track': 'Bikernieku Trase',
            },
            {
                'event': 'Drift Masters Round 6',
                'country': 'Germany',
                'date': '14-16.08.2025',
                'track': 'Ferropolis',
            },
            {
                'event': 'Drift Masters Round 7',
                'country': 'Poland',
                'date': '12-13.09.2025',
                'track': 'PGE Narodowy',
            },
        ]
    }

    return render(request, 'main/events.html', values)

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