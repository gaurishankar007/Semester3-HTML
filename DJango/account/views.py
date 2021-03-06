from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .auth import unauthenticated_user
from Product.models import Profile


@unauthenticated_user
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, username=user.username)
            messages.add_message(request, messages.SUCCESS, 'User Registered Successfully')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to Register User')
            return render(request, 'account/Register.html', {'form': form})
    context = {'form': UserCreationForm}
    return render(request, 'account/Register.html', context)


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                if not user.is_staff:
                    login(request, user)
                    return redirect('/product/django_web')
                elif user.is_staff:
                    login(request, user)
                    return redirect('/admins-dashboard')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password Invalid')
                return render(request, 'account/login.html', {'form': form})
    context = {'form': LoginForm}
    return render(request, 'account/Login.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')
