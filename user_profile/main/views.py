from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from main.forms import RegistrationForm
from main.models import UserProfile


# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    """
    Home page
    :param request:
    :return:
    """
    return render(request, "main/home.html")


def register(request: HttpRequest) -> HttpResponse:
    """
    Register a new user
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})
