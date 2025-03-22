from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from main.forms import RegisterForm, UserProfileForm, EditUserForm, LoginForm
from main.models import UserProfile


# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    """
    Home page
    :param request:
    :return:
    """
    return render(request, "main/home.html")


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Register a new user
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/auth_page.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Login a user
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'main/auth_page.html', {'form': form, 'page_title': 'Login'})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logout a user
    :param request:
    :return:
    """
    logout(request)
    return redirect("login")


def edit_user_profile_view(request: HttpRequest) -> HttpResponse:
    """
    Edit user profile page
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        user = profile.user
        if request.method == "POST":
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            account_form = EditUserForm(request.POST, instance=user)
            if profile_form.is_valid() and account_form.is_valid():
                account_form.save()
                profile_form.save()
                return redirect("home")
        else:
            profile_form = UserProfileForm(instance=profile)
            account_form = EditUserForm(instance=user)
        return render(request, 'main/edit_profile.html', {
            'account_form': account_form,
            'profile_form': profile_form,
        })
    else:
        return redirect("home")
