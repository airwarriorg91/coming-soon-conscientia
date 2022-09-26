from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def register(request):
    if request.user:
        if request.user.is_active:
            return redirect('home')
        else:
            return redirect('verification')
    else:
        return render(request, 'register.html')

def events(request):
    return render(request,'fork.html')

def register2(request):
    return HttpResponse('user = ' + str(request.user) + ' status = ' + str(request.user.is_active))
    #return render(request,'register2.html')

def verify(request):
    return render(request,'verification.html')
