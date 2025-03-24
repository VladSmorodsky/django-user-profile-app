from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from main.forms import RegisterForm, UserProfileForm, EditUserForm, LoginForm, ChangePasswordForm
from main.models import UserProfile


# Create your views here.

@login_required
def home(request: HttpRequest) -> HttpResponse:
    """
    Home page
    :param request:
    :return:
    """
    user_list = UserProfile.objects.exclude(pk=request.user.pk).all()
    return render(request, "main/home.html", {"user_list": user_list})


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
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user_object = User.objects.filter(email=email).first()
            try:
                user = authenticate(username=user_object.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "You are now logged in")
                    return redirect("home")
                else:
                    messages.error(request, "Invalid username or password")
            except AttributeError:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'main/auth_page.html', {'form': form, 'page_title': 'Login'})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logout a user
    :param request:
    :return:
    """
    logout(request)
    return redirect("login")


@login_required
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
                messages.success(request, "Profile updated successfully")
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


@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    """
    Change user password
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                request.user.set_password(form.cleaned_data["new_password"])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully")
                return redirect("home")
        else:
            form = ChangePasswordForm(request.user)
        return render(request, 'main/change_password.html', {'form': form})
    else:
        return redirect("home")


@login_required
def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    Profile view page
    :param request:
    :param username:
    :return:
    """
    try:
        user = get_object_or_404(User, username__iexact=username)
        return render(request, 'main/profile_page.html', {'profile': user.userprofile})
    except User.DoesNotExist:
        raise Http404("Page not found")


def handler404(request: HttpRequest, exception) -> HttpResponse:
    """
    Handle Not Found error
    :param request:
    :param exception:
    :return:
    """
    return render(request, '404.html', status=404)
