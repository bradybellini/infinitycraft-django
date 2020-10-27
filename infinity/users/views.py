from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash
)

from ratelimit.decorators import ratelimit

from .forms import UserLogin, UserSignUp, UserEmailChange, EditProfile
from .decorators import auth_redirect, allowed_users


# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, 'index.html')


@ratelimit(key='ip', rate='1/m')
@ratelimit(key='post:username')
@auth_redirect
def login_view(request):
    next = request.GET.get('next')
    form = UserLogin(request.POST or None)
    if form.is_valid():
        human = True
        # email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    else:
        context = {'form': form}
        return render(request, 'accounts/login.html', context)

    context = {'form': form}

    return render(request, 'accounts/login.html', context)


@ratelimit(key='ip', rate='1/m')
@ratelimit(key='post:username')
@auth_redirect
def signup_view(request):
    next = request.GET.get('next')
    form = UserSignUp(request.POST or None)
    if form.is_valid():
        human = True
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        group = Group.objects.get(name='member')
        user.set_password(password)

        user.save()
        user.groups.add(group)
        new_user = authenticate(username=user.username,
                                password=password, email=user.email)
        login(request, new_user)
        # messages.success(request, f'Account was create for {user.username}')
        if next:
            return redirect(next)
        return redirect('login')
    else:
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
        
    context = {'form': form}

    return render(request, 'accounts/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def profile_view(request):
    user = request.user
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('/account/profile/')
    else:
        form = EditProfile(instance=request.user)
        context = {"form": form}
        return render(request, 'accounts/edit_profile.html', context)
        
@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile/')
        else:
            return redirect('/account/change-password/')
    else:
        form = PasswordChangeForm(user=request.user)
        context = {"form": form}
        return render(request, 'accounts/change_password.html', context)