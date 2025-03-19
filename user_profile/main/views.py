from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from main.forms import RegistrationForm


# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    """
    Register a new user
    :param request:
    :return:
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})
