from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLogin, UserSignUp

def home(request):
    return render(request, 'index.html')

@ratelimit(key='ip', rate='1/m')
@ratelimit(key='post:username')
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
        
    context = {
        'form': form
    }   
        
    return render(request, 'accounts/login.html', context)

@ratelimit(key='ip', rate='1/m')
@ratelimit(key='post:username')
def signup_view(request):
    next = request.GET.get('next')
    form = UserSignUp(request.POST or None)
    if form.is_valid():
        human = True
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password, email=user.email)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
        
    context = {
        'form': form
    }   
        
    return render(request, 'accounts/signup.html', context)
    
def logout_view(request):
    logout(request)
    return redirect('/')
    
    
@login_required(login_url='/login/')
def profile_view(request):
    pass