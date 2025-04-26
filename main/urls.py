# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('events', views.events, name='events'),
    path('home', views.index, name='home'),
    path('contact', views.contact, name='contact'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html", success_url=reverse_lazy('password_change_done')))
]
