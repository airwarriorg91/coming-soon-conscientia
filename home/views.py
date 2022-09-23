from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def events(request):
    return render(request,'fork.html')

def register2(request):
    return render(request,'register2.html')

def verify(request):
    return render(request,'verification.html')