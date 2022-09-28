from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def register(request):
    if request.user.username:
        if request.user.is_active:
            return render(request,'events.html')
        else:
            return redirect('verification')
    else:
        return render(request, 'register.html')

def events(request):
    return render(request,'events.html')

def verify(request):
    return render(request,'verification.html')
